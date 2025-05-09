# Epigenetic Clock Database

A web application for exploring, analysing, and comparing DNA methylation age (DNAm age) clocks via a user-friendly interface. Users can upload methylation beta-value files, run supported clocks using the "dnaMethyAge" R package, visualise clock-specific statistics, and compute age predictions from different clocks with the same file.

### Features:

- **Clock Database** - browse and view information for each supported epigenetic clock.
- **Interactive Visualisations** - view clock-specific CpG breakdowns by CpG island context and UCSC annotation type.
- **Beta-Values Upload** - upload your own DNA methylation data (beta-values from CpG probe IDs).
- **Clock Predictions** - run multiple clocks simultaneously and receive biological age predictions, leveraging the [`dnaMethyAge`](https://github.com/yiluyucheng/dnaMethyAge) R package from [Wang et al., 2013](https://doi.org/10.1007/s11357-023-00871-w).

## Setup Instructions

### Prerequisites:
- Python 3.8+
- R (version compatible with `dnaMethyAge`)
- MongoDB running locally or remotely
- Required R packages (see `install_r_packages.R`)
- Required Python packages (see `requirements.txt`)

### 1. Clone the repository:
```bash
git clone https://github.com/Nicole-Forrester/clock-project
cd clock-project
```

### 2. Create a Python virtual environment:
Inside the clock-project folder, run:
```bash
python -m venv venv
```
Then activate the virtual environment on Windows:
```bash
venv\Scripts\activate.bat
```
or on Linux or Mac:
```bash
. venv/bin/activate
```

### 3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

#### (Alternative steps 2 and 3) Create and activate a Conda environment:
```bash
conda env create -f environment.yml
conda activate dev-clock
```

### 4. Install the required R packages:
```bash
Rscript install_r_packages.R
```

### 5. Create a config file
The config file, `configuration/conf.json` will contain the details of the installation. Edit the information to contain the details of your mongodb server: the address, and choose a username and password. Rename the file:
```bash
mv configuration/example_conf.json > configuration/conf.json
```

### 6. Set up the database using Python and MongoDB:
Create a user in the mongosh shell - the username and password must match what is in the `conf.json` file:
```bash
use clocks_database
db.createUser(
  {
    user: "username",
    pwd:  "p@ssw0rd",
    roles: [ { role: "readWrite", db: "clocks_database" }]
  }
)
```
Next run the setup script, which sets up the MongoDB collections:
```bash
python setup_database.py
```

### 7. Run the Flask web app:
```bash
cd www
python webapp.py
```


## Beta-Values File Upload Requirements:

Your input beta matrix should be in CSV format, with:
- Rows as CpG IDs (e.g., `cg00000029`)
- Columns as sample names

Example:
```bash
,sample1,sample2
cg00000029,0.76,0.81
cg00000108,0.45,0.51
...
```