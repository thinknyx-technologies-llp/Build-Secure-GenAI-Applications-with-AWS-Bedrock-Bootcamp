from processor import DocumentProcessor
processor = DocumentProcessor()
processor.process(
    pdf_path="sample_data/THINKNYX_HR_Policy_Compliance.pdf",
    doc_name="THINKNYX_HR_Policy_Compliance",
    bucket="thinknyx-hr-policy-compliance-docs"
)