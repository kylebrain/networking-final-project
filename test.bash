for i in {1..10}
do
python main.py config_files/config0.txt >> log_files/log_scalability1.txt &
python main.py config_files/config1.txt >> log_files/log_scalability2.txt &
python main.py config_files/config2.txt >> log_files/log_scalability3.txt &
python main.py config_files/config3.txt >> log_files/log_scalability4.txt
python main.py config_files/config4.txt >> log_files/log_scalability5.txt & 
python main.py config_files/config5.txt >> log_files/log_scalability6.txt &
python main.py config_files/config6.txt >> log_files/log_scalability7.txt &
python main.py config_files/config7.txt >> log_files/log_scalability8.txt
python main.py config_files/config8.txt >> log_files/log_scalability9.txt &
python main.py config_files/config9.txt >> log_files/log_scalability10.txt &
python main.py config_files/config10.txt >> log_files/log_scalability11.txt &
python main.py config_files/config11.txt >> log_files/log_scalability12.txt
python main.py config_files/config12.txt >> log_files/log_scalability13.txt &
python main.py config_files/config13.txt >> log_files/log_scalability14.txt &
python main.py config_files/config14.txt >> log_files/log_scalability15.txt &
python main.py config_files/config15.txt >> log_files/log_scalability16.txt
done