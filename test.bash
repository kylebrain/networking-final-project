for i in {1..10}
do
python main.py config_files/config0.txt >> log_files/log1.txt &
python main.py config_files/config1.txt >> log_files/log2.txt &
python main.py config_files/config2.txt >> log_files/log3.txt &
python main.py config_files/config3.txt >> log_files/log4.txt
python main.py config_files/config4.txt >> log_files/log5.txt & 
python main.py config_files/config5.txt >> log_files/log6.txt &
python main.py config_files/config6.txt >> log_files/log7.txt &
python main.py config_files/config7.txt >> log_files/log8.txt
python main.py config_files/config8.txt >> log_files/log9.txt &
python main.py config_files/config9.txt >> log_files/log10.txt &
python main.py config_files/config10.txt >> log_files/log11.txt &
python main.py config_files/config11.txt >> log_files/log12.txt
python main.py config_files/config12.txt >> log_files/log13.txt &
python main.py config_files/config13.txt >> log_files/log14.txt &
python main.py config_files/config14.txt >> log_files/log15.txt &
python main.py config_files/config15.txt >> log_files/log16.txt
done