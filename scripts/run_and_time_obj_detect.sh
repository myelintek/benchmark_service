export WORLD_SIZE=4
pushd pytorch
for ((rank=0;rank<WORLD_SIZE-1;rank++)); do
  time  RANK=$rank python tools/train_mlperf.py --local_rank $rank --config-file "configs/e2e_mask_rcnn_R_50_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 72 SOLVER.STEPS "(48, 64)" SOLVER.BASE_LR 0.0025 &
done
time  RANK=$(($WORLD_SIZE-1)) python tools/train_mlperf.py --local_rank $(($WORLD_SIZE-1)) --config-file "configs/e2e_mask_rcnn_R_50_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 72 SOLVER.STEPS "(48, 64)" SOLVER.BASE_LR 0.0025
popd
