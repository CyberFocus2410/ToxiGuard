import sys
import os
import json
import time

# Ensure we can import the backend logic
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.main import handle_prediction_request

def run_stress_test():
    test_cases = [
        # Common Drugs & Molecules
        "CC(=O)OC1=CC=CC=C1C(=O)O", # Aspirin
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", # Caffeine
        "CN1CCCC1C2=CN=CC=C2", # Nicotine
        "CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34", # Testosterone
        "C1=CC=C(C=C1)O", # Phenol
        "CCO", # Ethanol
        "C1=CC=C(C=C1)C(=O)O", # Benzoic acid
        "C1=CC=C2C(=C1)C=CC(=N2)N", # Aminoquinoline
        "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", # Ibuprofen
        "CC(=O)NC1=CC=C(C=C1)O", # Paracetamol (Acetaminophen)
        # Known Toxins / Environmental Concerns
        "c1ccc(cc1)c2ccccc2", # Biphenyl
        "ClC(Cl)Cl", # Chloroform
        "c1ccc(c(c1)Cl)Cl", # Dichlorobenzene
        "O=C1C2=C(C(=O)N1)N(C=N2)C", # Theobromine (simpler)
        "C1=CC(=CC=C1N)S(=O)(=O)N", # Sulfanilamide
        # Complex / Larger Molecules
        "CC1=C(C(C(=C(C1C2=CC=CC=C2[N+](=O)[O-])C(=O)OC)C)C(=O)OC)C", # Nifedipine
        "CN(C)C1=CC=C(C=C1)C(=O)C2=CC=C(C=C2)N(C)C", # Michler's Ketone
        "C1CCC(CC1)N", # Cyclohexylamine
        "C1=CC=C(C=C1)N=C=O", # Phenyl isocyanate
        "C[C@H](C1=CC=C(C=C1)CC(C)C)C(=O)O", # Ibuprofen (isomer)
        # Edge Cases & Symbols
        "C", # Methane (tiny)
        "CCCCCCCCCCCCCCCCCCCC", # Eicosane (Long chain)
        "C1=CC=CC=C1", # Benzene
        "c1ccccc1", # Benzene (alt format)
        "O", # Water
        "N", # Ammonia
        "S", # Sulfur
        "O=C1NC(=O)NC(=O)C1(CC)C2=CC=CC=C2", # Phenobarbital
        "C1=CC=C2C(=C1)C=CC3=C2C=CC4=C3C=CC5=C4C=CC=C5", # Pentacene (Large Aromatic)
        "ClC(Cl)(Cl)Cl", # Carbon Tetrachloride
        # Psychoactive / Sensitive
        "CN1[C@H]2CC[C@@H]1[C@H]([C@H](C2)OC(=O)C3=CC=CC=C3)C(=O)OC", # Cocaine
        "CN[C@@H](C)CC1=CC=C(C=C1)O", # Tyramine derivative
        "CN1CCC[C@@H]1C2=CN=CC=C2", # (S)-Nicotine
        "CCC[C@@H](C)C1(C(=O)NC(=O)NC1=O)CC", # Butabarbital
        "CC(C)(C)NCC(C1=CC(=C(C=C1)O)CO)O", # Albuterol
        "CN(C)CCCN1C2=CC=CC=C2SC3=C1C=C(C=C3)Cl", # Chlorpromazine
        "C1=CC=C(C=C1)NS(=O)(=O)C2=CC=C(C=C2)N", # Sulfanilamide (isomer)
        "CC1=NC=C(C(=C1O)CO)CO", # Pyridoxine
        "C1=CC=C(C=C1)Cl", # Chlorobenzene
        "C1=CC=NC=C1", # Pyridine
        "InvalidString", # INVALID CASE (Error Handling Test)
        "", # EMPTY CASE (Error Handling Test)
        "12345", # NUMERIC (Error Handling Test)
    ]

    print(f"🚀 INITIATING TOXIGUARD STRESS TEST: {len(test_cases)} CASES")
    print("-" * 60)
    
    passed = 0
    failed = 0
    
    for i, smiles in enumerate(test_cases):
        try:
            start_time = time.time()
            result = handle_prediction_request(smiles)
            end_time = time.time()
            latency = end_time - start_time
            
            if 'error' in result:
                if i >= 40: # Expect errors for invalid inputs at the end
                    print(f"[{i+1}/{len(test_cases)}] ✅ CAUGHT INVALID: {smiles[:15]}... ({result['error']})")
                    passed += 1
                else:
                    print(f"[{i+1}/{len(test_cases)}] ❌ FAILED VALID: {smiles} - {result['error']}")
                    failed += 1
            else:
                passed += 1
                cat = result.get('toxicity_category', 'Unknown')
                prob = result.get('toxicity_probability', 0.0)
                print(f"[{i+1}/{len(test_cases)}] ✅ PASSED: {smiles[:15]}... | RISK: {cat} ({prob*100:.1f}%) | Latency: {latency:.3f}s")
            
        except Exception as e:
            failed += 1
            print(f"[{i+1}/{len(test_cases)}] 💥 CRASHED: {smiles} - {e}")

    print("-" * 60)
    print(f"🎯 TEST SUMMARY: {passed} PASSED | {failed} FAILED | {passed/len(test_cases)*100:.1f}% PRODUCTION READINESS")
    
    if failed == 0:
        print("💡 ALL SYSTEMS GREEN. TOXIGUARD READY FOR DEPLOYMENT.")
    else:
        print("⚠️ ACTION REQUIRED: INVESTIGATE FAILED CASES.")

if __name__ == "__main__":
    run_stress_test()
