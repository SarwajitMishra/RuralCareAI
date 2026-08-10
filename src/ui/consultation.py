"""
Consultation UI

AI-Based Rural Healthcare Triage Assistant

Allows the healthcare worker to:

1. Select a patient
2. Select symptoms
3. Predict disease
4. View AI triage
5. Save consultation
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from src.utils.pdf_generator import PDFGenerator

from src.services.patient_service import PatientService
from src.services.consultation_service import ConsultationService
from src.nlp.symptom_extractor import SymptomExtractor
from src.ml.symptom_service import SymptomService


from src.image.image_service import ImageService
from src.voice.voice_service import VoiceService
import tempfile

from src.ml.predictor import DiseasePredictor
from src.image.image_predictor import ImagePredictor
from src.ml.fusion_engine import FusionEngine
from src.ml.risk_engine import RiskEngine
from src.ai.llm_service import LLMService
from src.knowledge.knowledge_base import KnowledgeBase

# ---------------------------------------------------------
# Services
# ---------------------------------------------------------

patient_service = PatientService()
consultation_service = ConsultationService()
symptom_service = SymptomService()
symptom_extractor = SymptomExtractor()
image_service = ImageService()
voice_service = VoiceService()
fusion_engine = FusionEngine()
llm_service = LLMService()
knowledge_base = KnowledgeBase()

# ---------------------------------------------------------
# ML Models
# ---------------------------------------------------------

disease_predictor = DiseasePredictor()
image_predictor = ImagePredictor()


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

DEFAULTS = {

    "consultation_prediction": None,

    "fusion_result": None,

    "knowledge": None,

    "ai_summary": None,

    "voice_transcript": None,

    "consultation_saved": False,

    "saved_pdf_path": None,

    "selected_patient_id": None,

    "selected_symptoms": [],

    "doctor_notes": "",

    "report_language": "English",
}

# Hindi/Hinglish support exists end-to-end (prompt, PDF Devanagari
# font), but gemma3:1b doesn't reliably honor the language instruction
# on a prompt this long - tested output came back as Spanish, German,
# and plain English across otherwise-identical runs. Restricted to
# English until a more capable local model is available.
REPORT_LANGUAGES = ["English"]

# ---------------------------------------------------------
# Main Screen
# ---------------------------------------------------------

def show_consultation():

    # Runs on every call (i.e. every rerun, for every session) rather
    # than at module level - module-level code only executes once per
    # server process (the first time this module is imported), so a
    # module-level init loop would leave session_state uninitialized
    # for every session after the first.
    for key, value in DEFAULTS.items():

        if key not in st.session_state:

            st.session_state[key] = value

    st.title("🩺 AI Consultation")

    st.caption(
        "AI-Based Rural Healthcare Triage Assistant"
    )

    patients = patient_service.get_all_patients()

    if not patients:

        st.warning(
            "No patients registered."
        )

        st.info(
            "Please register a patient first."
        )

        return

    st.divider()

    # -------------------------------------------------
    # Patient Selection
    # -------------------------------------------------

    st.subheader("👤 Select Patient")

    patient_options = {

        f"{patient.patient_code} - {patient.full_name}":
            patient.id

        for patient in patients

    }

    selected_label = st.selectbox(

        "Patient",

        list(patient_options.keys()),

    )

    patient_id = patient_options[selected_label]

    st.session_state.selected_patient_id = patient_id

    patient = patient_service.get_patient(patient_id)

    st.divider()

    # -------------------------------------------------
    # Patient Information
    #
    # Collapsed by default and bound to the selected patient's name -
    # click to expand for the full record instead of it always taking
    # up screen space. Chronic conditions and other medical history are
    # captured once at Patient Registration (not re-entered here); they
    # still feed the risk assessment below via patient.chronic_conditions
    # / patient.remarks.
    # -------------------------------------------------

    with st.expander(f"📋 Patient Details — {patient.full_name}"):

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(

                "Patient ID",

                patient.patient_code,

                disabled=True,

            )

            st.text_input(

                "Full Name",

                patient.full_name,

                disabled=True,

            )

            st.text_input(

                "Gender",

                patient.gender,

                disabled=True,

            )

            st.text_input(

                "Blood Group",

                patient.blood_group or "",

                disabled=True,

            )

            st.text_input(

                "Mobile",

                patient.mobile_number or "",

                disabled=True,

            )

        with col2:

            st.text_input(

                "Age",

                str(patient.age),

                disabled=True,

            )

            st.text_input(

                "Village",

                patient.village or "",

                disabled=True,

            )

            st.text_input(

                "District",

                patient.district or "",

                disabled=True,

            )

            st.text_input(

                "State",

                patient.state or "",

                disabled=True,

            )

            st.text_input(

                "Weight (kg)",

                str(patient.weight_kg or ""),

                disabled=True,

            )

        st.markdown("**Known Chronic Conditions**")

        st.write(patient.chronic_conditions or "None recorded")

        st.markdown("**Other Medical History / Remarks**")

        st.write(patient.remarks or "None recorded")

    medical_history = (
        [c.strip() for c in patient.chronic_conditions.split(",") if c.strip()]
        if patient.chronic_conditions else []
    )

    other_history = patient.remarks or ""

    st.divider()

    # -------------------------------------------------
    # Multimodal Symptom Input (Text / Voice / Image)
    #
    # All three modalities sit side by side in one row, matching the
    # architecture diagram's parallel-input framing, rather than being
    # tucked behind tabs. Columns don't create a separate Python scope,
    # so user_input / image_prediction are set exactly as before - just
    # presented as parallel panels instead of switchable tabs.
    # -------------------------------------------------

    st.subheader("🤒 Patient Symptoms & Media")

    st.caption(
        "Provide symptoms via text, voice, and/or a skin image - all "
        "three feed the same prediction, so combine as many as apply."
    )

    col_text, col_voice, col_image = st.columns([2, 1, 1])

    with col_text:

        st.markdown("**📝 Text**")

        user_input = st.text_area(

            "Describe the patient's symptoms",

            height=200,

            placeholder="""
    Examples:

    • I have fever and cough for 3 days

    • Bukhar hai aur ulti ho rahi hai

    • Repeated fever, loose motion and stomach infection

    • Chest pain with breathing difficulty
    """

        )

    with col_voice:

        st.markdown("**🎤 Voice (Optional)**")

        st.caption("Record live with the mic, as an alternative to typing.")

        voice_file = st.audio_input("Record symptoms")

        with st.expander("Or upload an audio file"):

            uploaded_audio = st.file_uploader(
                "Upload audio",
                type=["wav", "mp3", "m4a", "ogg"],
                label_visibility="collapsed",
            )

        audio_source = voice_file or uploaded_audio

        if audio_source:

            suffix = Path(
                getattr(audio_source, "name", "recording.wav")
            ).suffix or ".wav"

            with tempfile.NamedTemporaryFile(

                    delete=False,

                    suffix=suffix

            ) as tmp:
                tmp.write(audio_source.read())

                audio_path = tmp.name

            with st.spinner("Transcribing voice..."):
                voice_result = voice_service.transcribe(audio_path)

            st.success("✅ Voice successfully transcribed")

            st.text_area(

                "Transcript",

                value=voice_result["transcript"],

                height=100,

                disabled=True,

            )

            # Replace typed text with transcript

            user_input = voice_result["transcript"]

            st.session_state.voice_transcript = voice_result["transcript"]

    with col_image:

        st.markdown("**📷 Skin Image (Optional)**")

        uploaded_image = st.file_uploader(
            "Upload Skin Lesion",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
        )

        image_prediction = None

        if uploaded_image:

            st.image(
                uploaded_image,
                caption="Uploaded Image",
                use_container_width=True,
            )

            with st.spinner("Analyzing image..."):

                try:

                    image_prediction = image_service.predict(uploaded_image)

                    st.success(
                        f"Prediction: {image_prediction['prediction']}"
                    )

                    st.metric(
                        "Confidence",
                        f"{image_prediction['confidence'] * 100:.2f}%"
                    )

                except Exception as ex:

                    st.error(str(ex))

    st.write("")

    extract = st.button(
        "🔍 Extract Symptoms from Text / Voice",
        use_container_width=True,
    )

    if extract:

        result = symptom_extractor.extract(user_input)

        st.session_state.selected_symptoms = result["detected_symptoms"]

        st.session_state.nlp_result = result

    selected_symptoms = st.multiselect(

        "AI Extracted Symptoms (Editable)",

        symptom_service.get_machine_symptoms(),

        default=st.session_state.selected_symptoms,

        format_func=lambda x: x.replace("_", " ").title(),

        # A real consultation realistically involves a handful of
        # symptoms - this caps Streamlit's built-in "select all" (shown
        # automatically for long option lists) from producing a
        # nonsensical prediction off all 132 possible symptoms at once.
        max_selections=15,

    )

    st.session_state.selected_symptoms = selected_symptoms

    st.caption(
        "Click **Extract Symptoms** to auto-fill this list from the text "
        "or voice tab above, then add, remove, or correct any symptom "
        "before predicting - your edits here are what gets predicted on."
    )

    # Only English is offered for now (see REPORT_LANGUAGES) - a
    # single-option selector would just be clutter, so the language
    # plumbing (llm_service prompt, PDF Devanagari font) stays wired
    # up without a visible UI control until more languages are viable.
    report_language = REPORT_LANGUAGES[0]

    st.session_state.report_language = report_language

    st.divider()

    st.write("")

    predict = st.button(

        "🧠 Predict Disease",

        type="primary",

        use_container_width=True,

    )

    if predict:

        # Predicts on whatever is currently in the "AI Extracted
        # Symptoms (Editable)" list above - populated by "Extract
        # Symptoms" and/or manually edited by the healthcare worker.
        # Re-running extraction here would silently discard any
        # manual corrections, so it deliberately does not happen.

        selected_symptoms = st.session_state.selected_symptoms

        if len(selected_symptoms) == 0:

            st.error(
                "Please click 'Extract Symptoms from Text / Voice' first, "
                "or select at least one symptom manually."
            )

            return

        machine_symptoms = selected_symptoms

        # Symptom-based (Random Forest) prediction, enriched with a
        # preliminary risk assessment.
        prediction = consultation_service.predict(
            machine_symptoms,
            medical_history=medical_history,
        )

        # Multimodal late-fusion of the text and (optional) image
        # predictions into a single final result.
        fusion_result = fusion_engine.fuse(
            prediction,
            image_prediction
        )

        # Risk must reflect the FINAL fused disease, which can differ
        # from the text-only prediction when the image model overrides it.
        final_risk = RiskEngine.assess(
            disease=fusion_result["predicted_disease"],
            confidence=fusion_result["confidence"],
            medical_history=medical_history,
            symptoms=machine_symptoms,
        )

        fusion_result["risk_level"] = final_risk["level"]
        fusion_result["recommendation"] = final_risk["recommendation"]

        # Retrieve grounded healthcare knowledge (RAG) for the final
        # predicted disease.
        knowledge = knowledge_base.retrieve(fusion_result["predicted_disease"])

        # AI-assisted clinical summary via the local LLM (Gemma 3 / Ollama),
        # grounded with the retrieved knowledge.
        with st.spinner("Generating AI clinical summary..."):
            ai_summary = llm_service.generate_report(
                patient,
                machine_symptoms,
                fusion_result,
                knowledge,
                language=report_language,
            )

        st.session_state.consultation_prediction = prediction
        st.session_state.fusion_result = fusion_result
        st.session_state.knowledge = knowledge
        st.session_state.ai_summary = ai_summary

    # -------------------------------------------------
    # AI Prediction Result
    #
    # Reads from session_state (rather than being nested inside
    # "if predict:") so that it, and the Save/Clear/Doctor Notes
    # controls below it, keep rendering across reruns triggered by
    # OTHER widgets (e.g. clicking "Save Consultation" itself is a
    # separate rerun on which "predict" is False).
    # -------------------------------------------------

    prediction = st.session_state.consultation_prediction
    fusion_result = st.session_state.fusion_result
    knowledge = st.session_state.knowledge
    ai_summary = st.session_state.ai_summary

    if st.session_state.consultation_saved:

        # Persistent post-save screen: shown on every rerun (including
        # the one triggered by clicking "Download PDF Report" itself)
        # until the user explicitly starts a new consultation, so the
        # download button doesn't vanish after a single render.

        st.divider()

        st.success("✅ Consultation saved successfully.")

        pdf_path = st.session_state.saved_pdf_path

        if pdf_path and Path(pdf_path).exists():

            with open(pdf_path, "rb") as pdf:

                st.download_button(
                    "📄 Download PDF Report",
                    pdf,
                    file_name=Path(pdf_path).name,
                    mime="application/pdf",
                )

        if st.button("🆕 Start New Consultation", type="primary"):

            st.session_state.selected_symptoms = []
            st.session_state.consultation_prediction = None
            st.session_state.fusion_result = None
            st.session_state.knowledge = None
            st.session_state.ai_summary = None
            st.session_state.voice_transcript = None
            st.session_state.doctor_notes = ""
            st.session_state.consultation_saved = False
            st.session_state.saved_pdf_path = None

            st.rerun()

    elif prediction is not None:

        st.divider()

        header_col, discard_col = st.columns([4, 1])

        with header_col:

            st.subheader("🧠 AI Triage Result")

        with discard_col:

            # Deliberately placed far from "Save Consultation" at the
            # bottom of this section, rather than beside it, so a
            # mis-click can't discard a completed diagnosis.
            if st.button(
                "🗑️ Discard & Restart",
                use_container_width=True,
            ):
                st.session_state.selected_symptoms = []
                st.session_state.consultation_prediction = None
                st.session_state.fusion_result = None
                st.session_state.knowledge = None
                st.session_state.ai_summary = None
                st.session_state.voice_transcript = None
                st.session_state.doctor_notes = ""

                st.rerun()

        confidence = fusion_result["confidence"]
        risk = fusion_result["risk_level"]
        predicted_disease = fusion_result["predicted_disease"]

        if risk == "Critical":
            risk_color = "🔴"
        elif risk == "High":
            risk_color = "🟠"
        elif risk == "Medium":
            risk_color = "🟡"
        else:
            risk_color = "🟢"

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "Predicted Disease",
                predicted_disease,
            )

            hindi_name = knowledge.get("hindi")

            if hindi_name:
                st.caption(f"🇮🇳 {hindi_name}")

        with metric2:

            st.metric(
                "Confidence",
                f"{confidence:.2f} %",
            )

        with metric3:

            st.metric(
                "Risk Level",
                f"{risk_color} {risk}",
            )

        st.success(
            fusion_result["recommendation"]
        )

        if "image_prediction" in fusion_result:
            st.caption(
                f"Fusion source: {fusion_result['decision_source']} "
                f"(image predicted: {fusion_result['image_prediction']} "
                f"at {fusion_result['image_confidence']:.2f}%)"
            )

        st.subheader("🧠 Why did the AI predict this? (SHAP)")

        st.caption(
            "Per-prediction SHAP contribution of each selected symptom "
            "toward the symptom-based model's predicted disease. "
            "Positive values push toward the prediction, negative "
            "values push away from it."
        )

        explanation = disease_predictor.explain_prediction(
            st.session_state.selected_symptoms
        )

        if explanation:
            explanation_df = pd.DataFrame(explanation)

            explanation_df["Importance"] = explanation_df["Importance"].round(4)

            st.dataframe(
                explanation_df,
                use_container_width=True,
                hide_index=True,
            )

            st.bar_chart(
                explanation_df.set_index("Symptom")
            )

        # ---------------------------------------------
        # Knowledge Base (RAG)
        # ---------------------------------------------

        st.subheader("📚 Disease Information")

        know_col1, know_col2 = st.columns(2)

        with know_col1:

            st.markdown(f"**Description**\n\n{knowledge.get('description', 'N/A')}")

            st.markdown("**Precautions**")
            for item in knowledge.get("precautions", []):
                st.write(f"- {item}")

            st.markdown("**First Aid**")
            for item in knowledge.get("first_aid", []):
                st.write(f"- {item}")

        with know_col2:

            st.markdown(
                f"**When to consult a doctor**\n\n"
                f"{knowledge.get('when_to_consult', 'N/A')}"
            )

            st.markdown("**🚩 Emergency Warning Signs**")
            for item in knowledge.get("emergency_signs", []):
                st.error(item)

        # ---------------------------------------------
        # AI Clinical Summary (Local LLM)
        # ---------------------------------------------

        st.subheader("🤖 AI Clinical Summary")

        st.info(ai_summary)

        st.write("")

        # ---------------------------------------------
        # Risk Assessment
        # ---------------------------------------------

        if risk == "Critical":

            st.error(
                "🚨 CRITICAL RISK\n\nImmediate emergency medical attention is recommended."
            )

        elif risk == "High":

            st.warning(
                "⚠️ HIGH RISK\n\nRefer the patient to the nearest physician or hospital."
            )

        elif risk == "Medium":

            st.info(
                "🟡 MEDIUM RISK\n\nClinical evaluation and follow-up are recommended."
            )

        else:

            st.success(
                "🟢 LOW RISK\n\nHome care and routine monitoring are recommended."
            )

        # ---------------------------------------------
        # Doctor Notes
        # ---------------------------------------------

        st.subheader("📝 Doctor Notes")

        notes = st.text_area(
            "Clinical Notes",
            value=st.session_state.doctor_notes,
            height=150,
            placeholder="Enter observations, treatment advice, medicines etc.",
        )

        st.session_state.doctor_notes = notes

        save = st.button(
            "💾 Save Consultation",
            type="primary",
            use_container_width=True,
        )

        if save:

            try:

                # The saved record (DB + PDF) must reflect the FINAL
                # fused disease/confidence, not the text-only model's -
                # they can differ whenever the image model overrides the
                # text prediction (see fusion_engine.py).
                save_prediction_result = {
                    **prediction,
                    "predicted_disease": fusion_result["predicted_disease"],
                    "confidence": fusion_result["confidence"],
                    "risk_level": fusion_result["risk_level"],
                    "recommendation": fusion_result["recommendation"],
                }

                consultation_service.save_consultation(

                    patient_id=patient.id,

                    symptoms=st.session_state.selected_symptoms,

                    prediction_result=save_prediction_result,

                    doctor_notes=notes,

                    image_path=(
                        image_prediction["image_path"]
                        if image_prediction else None
                    ),

                    image_prediction=(
                        image_prediction["prediction"]
                        if image_prediction else None
                    ),

                    image_confidence=(
                        image_prediction["confidence"]
                        if image_prediction else None
                    ),

                    voice_transcript=st.session_state.voice_transcript,

                    fusion_prediction=(
                        fusion_result["predicted_disease"]
                        if image_prediction else None
                    ),

                    fusion_confidence=(
                        fusion_result["confidence"]
                        if image_prediction else None
                    ),

                    ai_summary=ai_summary,

                )

                reports_dir = Path("reports")

                reports_dir.mkdir(exist_ok=True)

                pdf_file = reports_dir / f"{patient.patient_code}.pdf"

                PDFGenerator.generate_consultation_report(

                    filename=str(pdf_file),

                    patient=patient,

                    prediction=save_prediction_result,

                    symptoms=st.session_state.selected_symptoms,

                    doctor_notes=notes,

                    explanation=explanation,

                    knowledge=knowledge,

                    ai_summary=ai_summary,

                    report_language=st.session_state.report_language,

                )

                st.session_state.consultation_saved = True
                st.session_state.saved_pdf_path = str(pdf_file)

                st.balloons()

                st.rerun()

            except Exception as ex:

                st.exception(ex)
