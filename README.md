# M2DS: Marker Management Database System
This application is a tool for managing the polymorphic data of markers in F2 or RILs population.

## REQUIREMENTS

### Software
- Python (3.6.3)
- SQLite3 (3.19.3)

### Python Packages

- Django (2.0.3)
- django-bootstrap4 (0.0.6)
- django-pandas (0.5.1)
- numpy (1.14.2)
- pandas (0.22.0)

---

## Getting M2DS

- Type command on terminal (using Git):  
`git clone https://github.com/qqep685d/M2DS.git`

- Go to [https://github.com/qqep685d/M2DS](https://github.com/qqep685d/M2DS)  
Click "Clone or download" and "Download ZIP"

---

## Basic Usage

1. Type command on terminal:  
`sh run_server.sh`

1. Go to the URL on web browser:  
`127.0.0.1:8000`

1. Use application "M2DS"  
    1. Click `Add Population`  
        Input each fields and click `OK`.  
        ("Name" and "Year" are required fields.)  

    1. `Upload` file and `Import` dataset into database  in M2DS.  
        `M2DS/samples/sample_dataset.txt` is an example file.  

    - View records: `Strains`, `Markers` and `MS Table`.

    - Edit / Delete records.

    - `Download` dataset.

---

## Dataset File

See the example files:  
`M2DS/samples/sample_dataset.txt` or `M2DS/samples/sample_dataset_add.txt`

- The first row is header line.  
    - The first column is "MARKER". (Don't change!)
    - The second column is "TYPE". (Don't change!)
    - The third column and later are "strain names". You can input arbitrary names.
- The second row and later are each values.
    - The first column is "marker name". You can input arbitrary names. But the duplicated names is not allowed.
    - The second column is "type of marker". Input `g` or `p`.  
        - `g`: Genotype (Genetic marker)
        - `p`: Phenotype (Trait)
    - The third column and later are "marker values of each strain" for the marker. Input `A`, `B`, `H` or `-`.  
        * Genotype
            - `A`: Homozygous genotype of Parent 1 allele
            - `B`: Homozygous genotype of Parent 2 allele
            - `H`: Heterozygous genotype  
            - `-`: missing genotype
        * Phenotype
            - Strings, Integer or Float etc.
            - `-`: missing value

---

## License

This software is released under the MIT License, see LICENSE.
