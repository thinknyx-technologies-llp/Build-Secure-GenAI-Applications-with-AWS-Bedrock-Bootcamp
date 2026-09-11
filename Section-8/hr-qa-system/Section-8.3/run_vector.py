from vector_store import VectorDBIntegrator
integrator = VectorDBIntegrator(
    bucket_name="thinknyx-hr-policy-compliance-docs",
    collection_endpoint="8x5ymmu9jd4t8stecpe6.aoss.us-east-1.on.aws"
    )
chunks=integrator.fetch_chunks(doc_name="THINKNYX_HR_Policy_Compliance")
integrator.index_chunks(chunks)