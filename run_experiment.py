"""
Few-Shot Learning Experiment: ACORD Form to Policy JSON Generation
This script demonstrates using an LLM to predict policy attributes from ACORD forms.
"""

import json
import os
from anthropic import Anthropic

def load_training_examples():
    """Load the first 5 ACORD forms and their corresponding policies as training examples."""
    training_data = []
    base_path = os.path.join(os.path.dirname(__file__), 'data')

    for i in range(1, 6):
        with open(os.path.join(base_path, f'acord_form_{i}.txt'), 'r') as f:
            acord_form = f.read()
        with open(os.path.join(base_path, f'policy_{i}.json'), 'r') as f:
            policy_json = f.read()
        training_data.append({
            'acord_form': acord_form,
            'policy_json': policy_json
        })
    return training_data

def load_test_case():
    """Load the 6th ACORD form (test case) and ground truth policy."""
    base_path = os.path.join(os.path.dirname(__file__), 'data')

    with open(os.path.join(base_path, 'acord_form_6.txt'), 'r') as f:
        test_acord = f.read()
    with open(os.path.join(base_path, 'policy_6.json'), 'r') as f:
        ground_truth = json.load(f)
    return test_acord, ground_truth

def create_prompt(training_data, test_acord):
    """Create the few-shot prompt for the LLM."""
    prompt = """You are an insurance underwriting expert. Your task is to generate a JSON policy representation based on an ACORD insurance application form.

I will show you 5 examples of ACORD forms and their corresponding policy JSON representations. Then, you will generate a policy JSON for a new ACORD form.

"""
    
    # Add training examples
    for i, example in enumerate(training_data, 1):
        prompt += f"=== EXAMPLE {i} ===\n\n"
        prompt += f"ACORD FORM:\n{example['acord_form']}\n\n"
        prompt += f"CORRESPONDING POLICY JSON:\n{example['policy_json']}\n\n"
        prompt += "=" * 80 + "\n\n"
    
    # Add test case
    prompt += """Now, based on the patterns you've observed in the examples above, generate a policy JSON for this new ACORD form:

TEST ACORD FORM:
"""
    prompt += test_acord
    prompt += "\n\nGenerate the policy JSON following the same structure and logic as the examples. Return ONLY the JSON, no additional text."
    
    return prompt

def generate_policy_with_claude(prompt, api_key):
    """Use Claude to generate the policy JSON."""
    client = Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def compare_policies(generated, ground_truth):
    """Compare generated policy with ground truth and calculate metrics."""
    
    def flatten_dict(d, parent_key='', sep='.'):
        """Flatten nested dictionary for easier comparison."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    gen_flat = flatten_dict(generated)
    truth_flat = flatten_dict(ground_truth)
    
    # Find common keys
    common_keys = set(gen_flat.keys()) & set(truth_flat.keys())
    gen_only_keys = set(gen_flat.keys()) - set(truth_flat.keys())
    truth_only_keys = set(truth_flat.keys()) - set(gen_flat.keys())
    
    # Calculate matches
    exact_matches = 0
    close_matches = 0
    mismatches = 0
    
    comparison_details = {
        'exact_matches': [],
        'close_matches': [],
        'mismatches': [],
        'missing_in_generated': [],
        'extra_in_generated': []
    }
    
    for key in common_keys:
        gen_val = gen_flat[key]
        truth_val = truth_flat[key]
        
        if gen_val == truth_val:
            exact_matches += 1
            comparison_details['exact_matches'].append({
                'field': key,
                'value': truth_val
            })
        elif isinstance(gen_val, (int, float)) and isinstance(truth_val, (int, float)):
            # Check if numeric values are close (within 10%)
            if abs(gen_val - truth_val) / truth_val <= 0.10:
                close_matches += 1
                comparison_details['close_matches'].append({
                    'field': key,
                    'generated': gen_val,
                    'ground_truth': truth_val
                })
            else:
                mismatches += 1
                comparison_details['mismatches'].append({
                    'field': key,
                    'generated': gen_val,
                    'ground_truth': truth_val
                })
        else:
            mismatches += 1
            comparison_details['mismatches'].append({
                'field': key,
                'generated': gen_val,
                'ground_truth': truth_val
            })
    
    # Track missing and extra fields
    for key in truth_only_keys:
        comparison_details['missing_in_generated'].append({
            'field': key,
            'ground_truth': truth_flat[key]
        })
    
    for key in gen_only_keys:
        comparison_details['extra_in_generated'].append({
            'field': key,
            'generated': gen_flat[key]
        })
    
    # Calculate metrics
    total_fields = len(truth_flat)
    accuracy = (exact_matches + close_matches) / total_fields if total_fields > 0 else 0
    
    metrics = {
        'total_fields_in_ground_truth': total_fields,
        'total_fields_in_generated': len(gen_flat),
        'exact_matches': exact_matches,
        'close_matches': close_matches,
        'mismatches': mismatches,
        'missing_fields': len(truth_only_keys),
        'extra_fields': len(gen_only_keys),
        'accuracy': accuracy,
        'exact_match_rate': exact_matches / total_fields if total_fields > 0 else 0
    }
    
    return metrics, comparison_details

def main():
    """Main experiment function."""
    print("=" * 80)
    print("FEW-SHOT LEARNING EXPERIMENT: ACORD FORM TO POLICY JSON")
    print("=" * 80)
    print()
    
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set your API key to run this experiment.")
        print("\nTo set the key, run:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")
        return
    
    print("Step 1: Loading training examples (5 ACORD forms + policies)...")
    training_data = load_training_examples()
    print(f"✓ Loaded {len(training_data)} training examples")
    print()
    
    print("Step 2: Loading test case (6th ACORD form)...")
    test_acord, ground_truth = load_test_case()
    print("✓ Test case loaded")
    print()
    
    print("Step 3: Creating few-shot prompt...")
    prompt = create_prompt(training_data, test_acord)
    print(f"✓ Prompt created ({len(prompt)} characters)")
    print()
    
    print("Step 4: Generating policy JSON with Claude...")
    try:
        generated_text = generate_policy_with_claude(prompt, api_key)
        
        # Extract JSON from response (in case there's extra text)
        start_idx = generated_text.find('{')
        end_idx = generated_text.rfind('}') + 1
        json_text = generated_text[start_idx:end_idx]
        
        generated_policy = json.loads(json_text)
        print("✓ Policy JSON generated successfully")
        print()
        
        # Save generated policy
        output_path = os.path.join(os.path.dirname(__file__), 'generated_policy_6.json')
        with open(output_path, 'w') as f:
            json.dump(generated_policy, f, indent=2)
        print("✓ Generated policy saved to: generated_policy_6.json")
        print()
        
    except Exception as e:
        print(f"✗ Error generating policy: {e}")
        return
    
    print("Step 5: Comparing generated policy with ground truth...")
    metrics, details = compare_policies(generated_policy, ground_truth)
    print()
    
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"Overall Accuracy: {metrics['accuracy']:.2%}")
    print(f"Exact Match Rate: {metrics['exact_match_rate']:.2%}")
    print()
    print(f"Total Fields (Ground Truth): {metrics['total_fields_in_ground_truth']}")
    print(f"Total Fields (Generated): {metrics['total_fields_in_generated']}")
    print()
    print(f"Exact Matches: {metrics['exact_matches']}")
    print(f"Close Matches: {metrics['close_matches']}")
    print(f"Mismatches: {metrics['mismatches']}")
    print(f"Missing Fields: {metrics['missing_fields']}")
    print(f"Extra Fields: {metrics['extra_fields']}")
    print()
    
    # Save detailed comparison
    output_path = os.path.join(os.path.dirname(__file__), 'comparison_results.json')
    with open(output_path, 'w') as f:
        json.dump({
            'metrics': metrics,
            'details': details
        }, f, indent=2)
    print("✓ Detailed comparison saved to: comparison_results.json")
    print()
    
    # Print sample mismatches
    if details['mismatches']:
        print("Sample Mismatches (first 5):")
        for mismatch in details['mismatches'][:5]:
            print(f"  • {mismatch['field']}")
            print(f"    Generated: {mismatch['generated']}")
            print(f"    Expected:  {mismatch['ground_truth']}")
        print()
    
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print()
    print("Files created:")
    print("  • generated_policy_6.json - The AI-generated policy")
    print("  • comparison_results.json - Detailed comparison metrics")

if __name__ == "__main__":
    main()
