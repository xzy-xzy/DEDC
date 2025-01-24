model="gpt-4o-2024-08-06"   # model evaluated
api_key="none"
python3 icl_eval.py --model $model --api_key $api_key
python3 icl_eval.py --show_primitive --model $model --api_key $api_key
python3 icl_eval.py --no_sys_gap --model $model --api_key $api_key
python3 icl_eval.py --no_sys_gap --show_primitive --model $model --api_key $api_key
python3 icl_eval.py --complete_sys_gap --model $model --api_key $api_key
python3 icl_eval.py --complete_sys_gap --show_primitive --model $model --api_key $api_key
python3 icl_eval.py --convert_symbol anom --model $model --api_key $api_key
python3 icl_eval.py --convert_symbol anom --show_primitive --model $model --api_key $api_key
python3 icl_eval.py --convert_symbol cross --model $model --api_key $api_key
python3 icl_eval.py --convert_symbol cross --show_primitive --model $model --api_key $api_key

