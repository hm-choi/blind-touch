import numpy as np
from seal import *
import asyncio
import aiohttp

SHARE_PATH = 'Path of the stored ciphertext from the main server \
             (The client\'s encrypted feature vector is given to the Main server, then the main server stored it in this path.)'
CLUSTERING_1 = 'Path of the cluster1 to save the result which is also used in the Main server'
CLUSTERING_2 = 'Path of the cluster2 to save the result which is also used in the Main server'
CLUSTERING_3 = 'Path of the cluster3 to save the result which is also used in the Main server'

RESULT = 'Path of the stored compressed result'
PK_PATH = 'Path of the public key from the client'
GK_PATH = 'Path of the galois key from the client'

parms = EncryptionParameters(scheme_type.ckks)
poly_modulus_degree = 16384
parms.set_poly_modulus_degree(poly_modulus_degree)
parms.set_coeff_modulus(CoeffModulus.Create(
        poly_modulus_degree, [60, 40, 40, 40, 60]))
scale = 2.0**40
context = SEALContext(parms)

ckks_encoder = CKKSEncoder(context)
slot_count = ckks_encoder.slot_count()
print(f'Number of slots: {slot_count}')

public_key = PublicKey()
public_key.load(context, PK_PATH)
galois_key = GaloisKeys()
galois_key.load(context, GK_PATH)
encryptor = Encryptor(context, public_key)
evaluator = Evaluator(context)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)   

urls = ['Cluseter1_IP:Cluseter1_Port/blindtouch', 'Cluseter2_IP:Cluseter1_Port/blindtouch', 'Cluseter3_IP:Cluseter3_Port/blindtouch']



def start_clustering():
    print('start')
    responses = asyncio.run(fetch_all(urls))
    print(responses)
    ctxt1 = Ciphertext()
    ctxt1.load(context, CLUSTERING_1)
    ctxt2 = Ciphertext()
    ctxt2.load(context, CLUSTERING_2)
    ctxt3 = Ciphertext()
    ctxt3.load(context, CLUSTERING_3)
 

    result = evaluator.add_many([ctxt1,ctxt2,ctxt3])
    result.save(RESULT)
    return RESULT
