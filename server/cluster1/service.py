
from seal import *
import keras
import tensorflow
from conf import *



parms = EncryptionParameters(scheme_type.ckks)
poly_modulus_degree = 16384
scale_val = poly_modulus_degree//2
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
relin_keys = RelinKeys()
relin_keys.load(context, RL_PATH)

encryptor = Encryptor(context, public_key)
evaluator = Evaluator(context)

model = keras.models.load_model(MODEL_PATH, custom_objects={'f1_m':f1_m, 'recall_m':recall_m, 'precision_m':precision_m})

weight = []
for w in model.get_weights()[32]:
    weight.append(w[0])
weight = ckks_encoder.encode(weight*512, scale)
bias_ = [model.get_weights()[33][0]]*8192
encoded_one_hot_vector = ckks_encoder.encode([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]*512, scale)

clustering_ctxt = Ciphertext()
clustering_ctxt.load(context, SAVED_CTXT1)

def square(evaluator, ctxt):
    temp = evaluator.multiply(ctxt, ctxt)
    evaluator.relinearize_inplace(temp, relin_keys)
    return temp

  
def fc1_layer(evaluator, ctxt):
    evaluator.rescale_to_next_inplace(ctxt)
    temp = encryptor.encrypt(weight)
    evaluator.mod_switch_to_inplace(temp, ctxt.parms_id())
    tmp1 = evaluator.multiply(ctxt, temp)
    evaluator.relinearize_inplace(tmp1, relin_keys)
    evaluator.rescale_to_next_inplace(tmp1)

    for i in range(4):
        tmp = evaluator.rotate_vector(tmp1, 2**i, galois_key)
        tmp1 = evaluator.add(tmp1, tmp)
    coeff = encryptor.encrypt(ckks_encoder.encode(bias_, tmp1.scale()))
    evaluator.mod_switch_to_inplace(coeff, tmp1.parms_id())
    tmp1 = evaluator.add(tmp1, coeff)

    coeff = encryptor.encrypt(encoded_one_hot_vector)
    evaluator.mod_switch_to_inplace(coeff, tmp1.parms_id())
    return evaluator.multiply(tmp1, coeff)
  

def start_clustering():
    ctxt = Ciphertext()
    ctxt.load(context, SHARE_PATH)
    sub_ctxt = evaluator.sub(ctxt, clustering_ctxt)
    result = fc1_layer(evaluator, square(evaluator, sub_ctxt))
    evaluator.relinearize_inplace(result, relin_keys)
    evaluator.rescale_to_next_inplace(result)
    result = evaluator.rotate_vector(result, (-1)*(CLUSTER_NUM-1), galois_key)
    result.save(CLUSTERING_1)
    return 'clustering_1'




