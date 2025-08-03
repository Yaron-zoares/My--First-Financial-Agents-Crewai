#!/usr/bin/env python3
# Change OpenAI Model Script
# סקריפט לשינוי מודל OpenAI

from model_config import get_model_info, set_model, estimate_cost

def main():
    """Main function to change the OpenAI model"""
    
    print("🤖 OpenAI Model Configuration")
    print("=" * 50)
    
    # Show available models
    get_model_info()
    
    print("\n💡 Model Recommendations:")
    print("• gpt-3.5-turbo: Best for cost-conscious users")
    print("• gpt-3.5-turbo-16k: Good for longer documents")
    print("• gpt-4-turbo-preview: High quality, reasonable cost")
    print("• gpt-4: Highest quality, most expensive")
    
    # Get user choice
    print("\n🔧 Choose a model:")
    print("1. gpt-3.5-turbo (cheapest)")
    print("2. gpt-3.5-turbo-16k (more memory)")
    print("3. gpt-4-turbo-preview (high quality)")
    print("4. gpt-4 (highest quality)")
    print("5. Show cost estimation")
    print("6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    model_mapping = {
        '1': 'gpt-3.5-turbo',
        '2': 'gpt-3.5-turbo-16k',
        '3': 'gpt-4-turbo-preview',
        '4': 'gpt-4'
    }
    
    if choice in model_mapping:
        model_name = model_mapping[choice]
        print(f"\n🔄 Setting model to: {model_name}")
        success = set_model(model_name)
        
        if success:
            print("✅ Model changed successfully!")
            print("💡 You can now run your financial analysis with the new model.")
        else:
            print("❌ Failed to change model")
    
    elif choice == '5':
        print("\n💰 Cost Estimation")
        print("-" * 30)
        
        # Example text lengths
        examples = [
            ("Short analysis (1,000 chars)", 1000),
            ("Medium report (5,000 chars)", 5000),
            ("Long document (20,000 chars)", 20000),
            ("Very long report (100,000 chars)", 100000)
        ]
        
        for description, length in examples:
            print(f"\n📄 {description}:")
            for model in ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-turbo-preview', 'gpt-4']:
                cost = estimate_cost(length, model)
                if cost:
                    print(f"   {model}: ${cost:.4f}")
    
    elif choice == '6':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 