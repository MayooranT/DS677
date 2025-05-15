## TO host the model

vllm serve bigcode/starcoder2-3b --dtype auto --api-key token-abc123

## TO run S->C

export OPENAI_API_KEY=token-abc123
export OPENAI_BASE_URL=http://localhost:8000/v1

python -m selfcodealign.src.star_align.self_ossinstruct   --seed_data_files "functions_with_return_cpp_filtered_100000_no_chuck/seed_functions_corrected.jsonl"   --max_new_data 100   --model bigcode/starcoder2-3b   --instruct_mode "S->C"   --save_dir "./outputs"

## To run C->I

python -m selfcodealign.src.star_align.self_ossinstruct \
  --seed_data_files "outputs/data-corrected-for-c2i.jsonl" \
  --max_new_data 100 \
  --model bigcode/starcoder2-3b \
  --instruct_mode "C->I" \
  --save_dir "./outputs"