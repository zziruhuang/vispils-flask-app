declare -A Config
Config=(
      [train_data_name]='tmModel/data-full/tmData-0809-descs5'
      [pred_data_name]='tmModel/data-full/tmData-0809-descs5-pred'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-3-2/'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-2-2-corr42/'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-2-2-corr42-dropout0.1'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-3'
      [checkpoint_path]='tmModel/corr-5-descs5-50-2-3-dropout0.05'
      [hidden_size]=50
      [depth]=2
      [ffn_num_layers]=3
)

# Config=(
#       #[train_data_name]='tmModel/subset/subset-br'
#       #[pred_data_name]='tmModel/subset/subset-br-pred'
#       #[checkpoint_path]='tmModel/corr-5-descs4-100-2-2-subset-Br/'
#       #[checkpoint_path]='tmModel/corr-5-descs4-100-2-2-subset-Br-corrdim42/'
#       #[train_data_name]='tmModel/subset-non-br'
#       #[pred_data_name]='tmModel/subset-non-br-pred'
#       #[checkpoint_path]='tmModel/corr-5-descs4-100-2-2-subset-nonBr/'
#       [hidden_size]=100
#       [ffn_num_layers]=2
#       [depth]=2
# )

Config=(
      [train_data_name]='tmModel/subset/subset-br-descs5'
      [pred_data_name]='tmModel/subset/subset-br-descs5-pred'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-2-2-subset-Br-corrdim42'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-2-subset-Br-corrdim42'
      [checkpoint_path]='tmModel/corr-5-descs5-br-hyperopt/depth_3_dropout_0.0_ffn_num_layers_2_hidden_size_96'

      #[train_data_name]='tmModel/subset/subset-non-br-descs5'
      #[pred_data_name]='tmModel/subset/subset-non-br-descs5-pred'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-2-2-subset-nonBr-corrdim42'

      [hidden_size]=96
      [ffn_num_layers]=2
      [depth]=3
)

Config=(
      [train_data_name]='tmModel/subset/subset-noother-descs5'
      [pred_data_name]='tmModel/subset/subset-noother-descs5-pred'
      #[checkpoint_path]='tmModel/corr-5-descs5-100-2-2-subset-noother'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-2-subset-noother'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-2-subset-noother-dropout0.1'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-3-subset-noother'
      #[checkpoint_path]='tmModel/corr-5-descs5-50-2-3-subset-noother-dropout0.05'
      #[checkpoint_path]='tmModel/corr-5-descs5-noother-hyperopt/depth_3_dropout_0.1_ffn_num_layers_3_hidden_size_96'
      [checkpoint_path]='tmModel/corr-5-descs5-noother-hyperopt/depth_2_dropout_0.0_ffn_num_layers_3_hidden_size_32'

      # [train_data_name]='tmModel/subset/subset-noother'
      # [pred_data_name]='tmModel/subset/subset-noother-pred'
      # [checkpoint_path]='tmModel/corr-5-descs4-noother-hyperopt/depth_3_dropout_0.05_ffn_num_layers_3_hidden_size_32'
      [hidden_size]=32
      [depth]=3
      [ffn_num_layers]=3
)


num_folds=4
gpu=0

i=0
pred_data_path="${Config[pred_data_name]}-smis.csv"
pred_features_path="${Config[pred_data_name]}-descs.csv"

for (( i=0; i<num_folds; i++)); do
    #i=$((i+1))
    ckptPath="${Config[checkpoint_path]}/fold_${i}"
    python -u predict.py \
       --data_path $pred_data_path \
       --features_path $pred_features_path \
       --checkpoint_path $ckptPath \
       --save_dir $ckptPath \
       --hidden_size ${Config[hidden_size]} \
       --depth ${Config[depth]} \
       --ffn_num_layers ${Config[ffn_num_layers]}\
       --gpu $gpu

done

