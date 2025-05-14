## TO run S->C

python -m selfcodealign.src.star_align.self_ossinstruct   --seed_data_files "functions_with_return_cpp_filtered_100000_no_chuck/seed_functions.jsonl"   --max_new_data 100   --model dummy   --instruct_mode "S->C"   --save_dir "./outputs"

## TO host the model

vllm serve bigcode/starcoder2-3b --dtype auto --api-key token-abc123