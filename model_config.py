# Model Configuration for Financial Analysis CrewAI System
# הגדרות מודלים למערכת ניתוח פיננסי CrewAI

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Available models with their costs and characteristics
MODEL_CONFIGS = {
    'gpt-3.5-turbo': {
        'name': 'gpt-3.5-turbo',
        'cost_per_1k_tokens': 0.002,  # $0.002 per 1K tokens
        'max_tokens': 4096,
        'description': 'Fast and cost-effective, good for basic tasks',
        'recommended_for': 'Basic financial analysis, simple calculations'
    },
    'gpt-3.5-turbo-16k': {
        'name': 'gpt-3.5-turbo-16k',
        'cost_per_1k_tokens': 0.003,  # $0.003 per 1K tokens
        'max_tokens': 16384,
        'description': 'More memory for longer texts, still cost-effective',
        'recommended_for': 'Complex financial reports, long documents'
    },
    'gpt-4': {
        'name': 'gpt-4',
        'cost_per_1k_tokens': 0.03,   # $0.03 per 1K tokens
        'max_tokens': 8192,
        'description': 'Highest quality, most expensive',
        'recommended_for': 'Complex analysis, high accuracy required'
    },
    'gpt-4-turbo-preview': {
        'name': 'gpt-4-turbo-preview',
        'cost_per_1k_tokens': 0.01,   # $0.01 per 1K tokens
        'max_tokens': 128000,
        'description': 'High quality, more affordable than GPT-4',
        'recommended_for': 'Advanced analysis, large datasets'
    }
}

def set_model(model_name='gpt-3.5-turbo'):
    """
    Set the OpenAI model for the application
    
    Args:
        model_name (str): Name of the model to use
    """
    if model_name not in MODEL_CONFIGS:
        print(f"❌ Model '{model_name}' not found. Available models:")
        for model in MODEL_CONFIGS.keys():
            print(f"  - {model}")
        return False
    
    # Set environment variables
    os.environ["OPENAI_MODEL_NAME"] = model_name
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
    # Get model info
    model_info = MODEL_CONFIGS[model_name]
    
    print(f"✅ Model set to: {model_name}")
    print(f"💰 Cost: ${model_info['cost_per_1k_tokens']:.3f} per 1K tokens")
    print(f"📝 Description: {model_info['description']}")
    print(f"🎯 Recommended for: {model_info['recommended_for']}")
    
    return True

def get_model_info(model_name=None):
    """
    Get information about available models or specific model
    
    Args:
        model_name (str, optional): Specific model name
    """
    if model_name:
        if model_name in MODEL_CONFIGS:
            return MODEL_CONFIGS[model_name]
        else:
            print(f"❌ Model '{model_name}' not found")
            return None
    
    print("📋 Available Models:")
    print("=" * 60)
    
    for name, config in MODEL_CONFIGS.items():
        print(f"🤖 {name}")
        print(f"   💰 Cost: ${config['cost_per_1k_tokens']:.3f} per 1K tokens")
        print(f"   📝 {config['description']}")
        print(f"   🎯 {config['recommended_for']}")
        print(f"   📊 Max tokens: {config['max_tokens']:,}")
        print("-" * 60)

def estimate_cost(text_length, model_name='gpt-3.5-turbo'):
    """
    Estimate the cost for processing text
    
    Args:
        text_length (int): Length of text in characters
        model_name (str): Model to use for estimation
    
    Returns:
        float: Estimated cost in USD
    """
    if model_name not in MODEL_CONFIGS:
        print(f"❌ Model '{model_name}' not found")
        return None
    
    # Rough estimation: 1 token ≈ 4 characters
    estimated_tokens = text_length / 4
    cost_per_1k = MODEL_CONFIGS[model_name]['cost_per_1k_tokens']
    
    estimated_cost = (estimated_tokens / 1000) * cost_per_1k
    
    return estimated_cost

# Set default model
DEFAULT_MODEL = 'gpt-3.5-turbo'

if __name__ == "__main__":
    # Show available models
    get_model_info()
    
    print(f"\n🔧 Setting default model: {DEFAULT_MODEL}")
    set_model(DEFAULT_MODEL) 