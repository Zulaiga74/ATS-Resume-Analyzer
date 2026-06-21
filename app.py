import streamlit as st 
from PyPDF2 import PdfReader
import plotly.express as px

st.title("AI Resume Analyzer")
st.markdown("""
            Analyze your Resume and get:
            
            ✅ ATS Score

            ✅ Skill Detection

            ✅ Missing Skills

            ✅ Recommendations
            """)

upload_file = st.file_uploader(
    "Choose your resume(PDF only)",
    type = ["pdf"]
)

if upload_file is not None:
    st.success("Resume uploaded successfully!")
    
    pdf_reader = PdfReader(upload_file)
    
    resume_text = " "
    
    for page in pdf_reader.pages:
        resume_text+=page.extract_text()
        
    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content",resume_text,height=300)
    
    skills = [
        "Python",
        "SQL",
        "Streamlit",
        "Pandas",
        "Machine Learning",
        "Power BI",
        "Excel"
    ]
    found_skills = []
    
    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)
    ats_score = (len(found_skills)/len(skills))*100
    
    
    
    st.subheader("ATS Score")
    st.progress(int(ats_score))
    st.write(f"ATS Score: {ats_score:.0f}%")
    
    st.subheader("Skills Found")
    
    for skill in found_skills:
        st.success(skill)
        
    missing_skills=[]
    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)
    st.subheader("Missing Skills")
    
    for skill in missing_skills:
        st.warning(skill)
        
    st.subheader("Recommendations")
    if missing_skills:
        st.write("Consider adding these skills to improve your ATS score:")
        
        for skill in missing_skills:
            st.write(f". {skill}")
    else:
        st.success("Excellent! All target skills are present.")
        
    col1,col2,col3 = st.columns(3)
    col1.metric("ATS Score",f"{ats_score:.0f}%")
    col2.metric("Skills Found",len(found_skills))
    col3.metric("Skills Missing",len(missing_skills))
    
    data = {
        "Category":["Found Skills","Missing Skills"],
        "Count":[len(found_skills),len(missing_skills)]
    }
    
    fig= px.pie(
        values = data["Count"],
        names=data["Category"],
        title="Skills Analysis"
    )
    st.plotly_chart(fig)
    
    report = f"""
    ATS Score: {ats_score:.0f}%
    Skills Found:
    {','.join(found_skills)}
    Missing Skills:
    {','.join(missing_skills)}
    """
    
    st.download_button(
        label = "Download Report",
        data = report,
        file_name="resume_analysis_report.pdf",
        mime="text/plain"
    )
    
