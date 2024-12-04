from recommender.stamp_recommender import StampRecommender
import pandas as pd

def main():
    df = pd.read_csv('stamps_data_21to24.csv')
    
    recommender = StampRecommender(df)
    
    while True:
        stamp_name = input("\nEnter the name of the stamp you want recommendations for: ")
        
        recommendations = recommender.get_recommendations(stamp_name)
        
        if len(recommendations) > 0:
            print("\nRecommended stamps that share similar words:")
            print(recommendations)
        else:
            print("\nNo similar stamps found.")
        
        continue_search = input("\nWould you like to search for another stamp? (yes/no): ").lower()
        if continue_search != 'yes':
            break
    
    print("\nThank you for using the stamp recommendation system!")

if __name__ == "__main__":
    main() 