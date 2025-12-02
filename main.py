import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO
import tempfile
import os

def create_sample_graphs():
    # Generate sample data
    x = np.arange(0, 70)
    y1 = 500 + 30 * np.sin(x / 8)
    y2 = 200 + 30 * np.cos(x / 10)
    y3 = 450 + 20 * np.abs(np.sin(x / 18))

    temp_files = []

    # 1. Upper body vertical position chart
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y1, color='orange')
    ax1.set_xlabel("Frames")
    ax1.set_ylabel("Y-coordinates")
    ax1.set_title("Upper Body Vertical Position")
    tmp1 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig1.savefig(tmp1.name, format="png", bbox_inches='tight')
    temp_files.append(tmp1.name)
    plt.close(fig1)

    # 2. Knee joint angles chart
    fig2, ax2 = plt.subplots()
    ax2.plot(x, y2, label="Right Knee")
    ax2.plot(x, y2-20, label="Left Knee")
    ax2.set_xlabel("Frames")
    ax2.set_ylabel("Angle (deg)")
    ax2.set_title("Knee Joint Angles")
    ax2.legend()
    tmp2 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig2.savefig(tmp2.name, format="png", bbox_inches='tight')
    temp_files.append(tmp2.name)
    plt.close(fig2)

    # 3. Hip joint angles chart
    fig3, ax3 = plt.subplots()
    ax3.plot(x, y3, label="Right Hip")
    ax3.plot(x, y3-10, label="Left Hip")
    ax3.set_xlabel("Frames")
    ax3.set_ylabel("Angle (deg)")
    ax3.set_title("Hip Joint Angles")
    ax3.legend()
    tmp3 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig3.savefig(tmp3.name, format="png", bbox_inches='tight')
    temp_files.append(tmp3.name)
    plt.close(fig3)

    return temp_files

def generate_pdf(patient_id, session_notes, image_paths):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 12, "Physiotherapy Exercise Report", ln=1, align="C")
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Patient ID: {patient_id}", ln=1)
    pdf.cell(0, 8, f"Session Notes: {session_notes}", ln=1)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 6, "Summary:", ln=1)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 6, "Sample analysis results: Patient performed squats/lunges. "
                         "Knee/hip joint angles tracked, with vertical displacement showing good form. "
                         "Consistency between frames was within optimal clinical range. "
                         "No abnormal gait detected. (This is sample data)")

    for img_path in image_paths:
        pdf.ln(8)
        pdf.image(img_path, w=160)
        pdf.ln(2)

    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Report generated: Streamlit Demo", ln=1, align="R")

    # Use dest='S' to get bytes instead of writing to file
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output = BytesIO(pdf_bytes)

    # Cleanup temp files
    for f in image_paths:
        os.remove(f)
    return pdf_output

# ---- Streamlit UI ----
st.set_page_config(page_title="Physiotherapy Angle Detection", layout="wide")
st.title("Automated Physiotherapy Pose & Angle Analysis Platform")

with st.sidebar:
    st.header("Patient/Session Info")
    patient_id = st.text_input("Patient ID / Name")
    session_notes = st.text_area("Session Notes (optional)")

st.header("1. Upload Exercise Video")
uploaded_file = st.file_uploader("Upload your exercise video (MP4/AVI)", type=['mp4', 'avi'])

if uploaded_file:
    st.video(uploaded_file)
    if st.button("Generate Demo Analysis Report"):
        with st.spinner("Analyzing (sample demo)..."):
            image_paths = create_sample_graphs()
            pdf_file = generate_pdf(patient_id, session_notes, image_paths)
            st.success("Demo analysis complete! Download the PDF below.")
            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name=f"{patient_id}_physio_report.pdf" if patient_id else "physio_report.pdf",
                mime="application/pdf",
            )



# import streamlit as st
# import requests

# st.set_page_config(page_title="Physiotherapy Angle Detection", layout="wide")
# st.title("Automated Physiotherapy Pose & Angle Analysis Platform")

# with st.sidebar:
#     st.header("Patient/Session Info")
#     patient_id = st.text_input("Patient ID / Name")
#     session_notes = st.text_area("Session Notes (optional)")

# st.header("1. Upload Exercise Video")
# uploaded_file = st.file_uploader("Upload your exercise video (MP4/AVI)", type=['mp4', 'avi'])

# if uploaded_file:
#     st.video(uploaded_file)
#     if st.button("Submit for Analysis"):
#         with st.spinner("Processing... (this may take a while)"):
#             files = {'video': (uploaded_file.name, uploaded_file, uploaded_file.type)}
#             data = {"patient_id": patient_id, "notes": session_notes}
#             response = requests.post("http://localhost:8000/process_video/", files=files, data=data)
#             if response.ok:
#                 results = response.json()
#                 st.success("Analysis complete!")
#                 st.write("### Key Results")
#                 st.json(results["angles"])   # Display joint angles
#                 st.markdown("#### Download Clinical Report")
#                 st.download_button(
#                     label="Download PDF Report",
#                     data=requests.get(results["pdf_url"]).content,
#                     file_name=f"{patient_id}_physio_report.pdf",
#                     mime="application/pdf",
#                 )
#             else:
#                 st.error(f"Failed: {response.text}")
