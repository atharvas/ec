singularity_base_command = "srun --job-name=logo_language_{} --output=jobs/{} --ntasks=1 --mem-per-cpu=10000 --gres=gpu --cpus-per-task 24 --time=10000:00 --qos=tenenbaum --partition=tenenbaum singularity exec -B /om2  --nv ../dev-container.img "

experiment_commands = []
jobs = []
job = 0

# Generates EC baseline experiments
RUN_EC_BASELINES = True
for enumerationTimeout in [1800, 3600]:
    job_name = "logo_ec_cnn_compression_et_{}".format(enumerationTimeout)
    jobs.append(job_name)
    
    num_iterations = 5
    task_batch_size = 40
    test_every = 3 # Every 120 tasks 
    base_parameters = "--no-cuda --enumerationTimeout {} --testingTimeout {} --recognitionEpochs 10 --biasOptimal --contextual --Helmholtz 0.5 --iterations {} --taskBatchSize {} --testEvery {}".format(enumerationTimeout, enumerationTimeout, num_iterations, task_batch_size, test_every)
    
    base_command = "python bin/logo.py "
    
    singularity = singularity_base_command.format(job, job_name)
    command = singularity + base_command + base_parameters + " &"
    if RUN_EC_BASELINES:
        experiment_commands.append(command)
    job += 1
for enumerationTimeout in [1800, 3600]:
    job_name = "logo_ec_compression_et_{}".format(enumerationTimeout)
    jobs.append(job_name)
    
    num_iterations = 5
    task_batch_size = 40
    test_every = 3 # Every 120 tasks 
    base_parameters = "--no-recognition --no-cuda --enumerationTimeout {} --testingTimeout {} --recognitionEpochs 10 --biasOptimal --contextual --Helmholtz 0.5 --iterations {} --taskBatchSize {} --testEvery {}".format(enumerationTimeout, enumerationTimeout, num_iterations, task_batch_size, test_every)
    
    base_command = "python bin/logo.py "
    
    singularity = singularity_base_command.format(job, job_name)
    command = singularity + base_command + base_parameters + " &"
    if RUN_EC_BASELINES:
        experiment_commands.append(command)
    job += 1
for enumerationTimeout in [1800, 3600]:
    job_name = "logo_ec_cnn_et_{}".format(enumerationTimeout)
    jobs.append(job_name)
    
    num_iterations = 5
    task_batch_size = 40
    test_every = 3 # Every 120 tasks 
    base_parameters = "--no-consolidation --no-cuda --enumerationTimeout {} --testingTimeout {} --recognitionEpochs 10 --biasOptimal --contextual --Helmholtz 0.5 --iterations {} --taskBatchSize {} --testEvery {}".format(enumerationTimeout, enumerationTimeout, num_iterations, task_batch_size, test_every)
    
    base_command = "python bin/logo.py "
    
    singularity = singularity_base_command.format(job, job_name)
    command = singularity + base_command + base_parameters + " &"
    if RUN_EC_BASELINES:
        experiment_commands.append(command)
    job += 1
    
#### Outputs
PRINT_LOG_SCRIPT = False
PRINT_JOBS = True
if PRINT_JOBS and not PRINT_LOG_SCRIPT:
    # print the jobs.
    print('#!/bin/bash')
    print("module add openmind/singularity")
    for command in experiment_commands:
        print(command + "")
        
if PRINT_LOG_SCRIPT:
    for job_name in jobs:
        print("echo 'Job: jobs/{} '".format(job_name))
        print("echo 'Training tasks:' ".format(job_name))
        print("grep 'total hit tasks' jobs/{}".format(job_name))
        print("echo 'Testing tasks:' ".format(job_name))
        print("grep 'testing tasks' jobs/{}".format(job_name))
        # Error checking
        print("grep 'OSError' jobs/{}".format(job_name))
        print("grep 'slurmstepd' jobs/{}".format(job_name))