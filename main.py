import os
import sys
import pandas as pd

# Ability to use Data Collection Functions 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "Data_Collection"))

# Imports of subfolders of Functions 
from Data_Collection.merge_data import merge_data  
from Data_Collection.processing_data import create_processed_data 
from Model_Building.Value_Score import create_value_score
from Model_Building.Cost_Features import cost_feature
from Model_Building.Market_Value import fit_market_model 
from Model_Building.Contract_Surplus import calculate_contract_suprlus
from Simulation.Monte_Carlo import run_monte_carlo       
from Visualization.Model_Evaluation import run_evaluation

def main():
    print("NBA PLAYER VALUATION & RISK PIPELINE")

    # Reference path for Readability 
    data_path = "Data/processed_data.csv"
    model_data_path = "Data/model_data.csv"
    final_risk_path = "Data/player_risk.csv"

    # Auto-create output directories to prevent save errors
    os.makedirs("Data", exist_ok=True)
    os.makedirs("Images", exist_ok=True)

    # Data Processing 
    print("\nBuilding and Refreshing processed dataset")
    try:
        raw_salaries = pd.read_csv("Data/salaries.csv", sep="\t", encoding="utf-8")
        raw_stats = pd.read_csv("Data/Stats_NBA.csv")
        merge_data(raw_salaries, raw_stats) 
        create_processed_data()

    except Exception as e:
        print("Continuing pipeline with existing file if available...")

    df = pd.read_csv(data_path)
    print(f"\nLoaded baseline dataset with {len(df)} players.")

    # Model Builiding 
    print("\nEngineering valuation features...")
    df = create_value_score(df)
    df = cost_feature(df)

    print("\nFitting market valuation model")
    df, model = fit_market_model(df)

    print("\nAnalyzing contract surplus values...")
    df = calculate_contract_suprlus(df)

    df.to_csv(model_data_path, index=False)
    print(f"Saved intermediate data to {model_data_path}")

    # Simulation of Players & Team Risk
    print("\nRunning Monte Carlo risk simulations...")
    player_risk = run_monte_carlo(df)

    print("\nMerging risk assessment with player metrics...")
    cols_to_merge = ["Player", "ValueScore", "ValuePerMillion"]
    player_risk = player_risk.merge(df[cols_to_merge], on="Player", how="left")

    player_risk.to_csv(final_risk_path, index=False)
    print(f"Saved simulated risk profiles to {final_risk_path}")

    # Visuals 
    print("\nGenerating evaluation plots and risk charts")
    try:
        run_evaluation() 
    except Exception as e:
        print(f"Note: Visualization generation skipped or experienced an error ({e})")

    # Final Outputs 
    print("\n" + "=" * 60)
    print("PIPELINE OUTPUT FILES")
    print("=" * 60)
    print(f" {data_path} — Input: Baseline player data")
    print(f" {model_data_path} — Output: Valuation model metrics")
    print(f" {final_risk_path} — Output: Simulated risk profiles")
    print(" Images/ — Output: Analytical diagnostic charts")
    
    print("\nEvaluation Complete")


if __name__ == "__main__":
    main()