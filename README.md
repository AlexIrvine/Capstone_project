# Whale GPS Movement Analytics Platform

This project processes open-source whale GPS datasets from the Movebank platform to create an interactive tracking and analytics application. The aim is to build an engaging and visually appealing application whilst also demonstrating robust ETL concepts. 


## Data

The full data set used can be found here: 
[Whale GPS Dataset](https://docs.google.com/spreadsheets/d/1yhXo8Khho4d0pMaciq60L1I5PeiGx6V4G4Gbe9LgjuQ/edit?gid=0#gid=0)

I downloaded the data with anomalies retained to show sufficient transformation techniques. Pipeline has not been tested on other data.
Save this data in the Capstone_project/data/raw folder. 

## Environment set up 

Built using Python 3.13.9

### 1. Create a virtual environment

```bash
python -m venv .venv 
```
### 2. Create a virtual environment

```bash
source .venv/Scripts/activate # Windows

source .venv/bin/activate # Mac
```
### 3. Install the dependencies

```bash
pip install -r e.

pip install -r requirements-setup.txt

```
### 4. To run the app 

```bash
streamlit run scr/streamlit/app.py

```






## Citations for data used in the study

### 1. Antarctic blue whales, east Antarctic sector of the Southern Ocean
**Citation:**  
Andrews-Goff V, Bell EM, Miller BS, Wotherspoon SJ, Double MC. 2022. Satellite tag derived data from two Antarctic blue whales (Balaenoptera musculus intermedia) tagged in the east Antarctic sector of the Southern Ocean. *Biodiversity Data Journal*. 10:e94228. https://doi.org/10.3897/BDJ.10.e94228

---

### 2. Azores Great Whales Satellite Telemetry Program
**Citations:**  
Silva MA et al. 2013. North Atlantic blue and fin whales suspend their spring migration to forage in middle latitudes: building up energy reserves for the journey. *PLoS ONE*. 8:e76507.  
Silva MA et al. 2014. Assessing performance of Bayesian state-space models fit to Argos satellite telemetry locations processed with Kalman filtering. *PLoS ONE*. 9:e92277.  
Prieto R et al. 2014. Sei whale movements and behaviour in the North Atlantic inferred from satellite telemetry. *Endangered Species Research*. 26:103–113.

---

### 3. Blue and fin whales Southern California 2014–2015 (Argos)
**Citation:**  
Irvine LM, Winsor MH, Follett TM, Mate BR, Palacios DM. 2020. An at-sea assessment of Argos location accuracy for three species of large whales, and the effect of deep-diving behavior on location error. *Animal Biotelemetry*. 8:20. doi: 10.1186/s40317-020-00207-x

---

### 4. Blue and fin whales Southern California 2014–2015 (Fastloc GPS)
**Citation:**  
Irvine LM, Palacios DM, Lagerquist BA, Mate BR. 2019. Scales of blue and fin whale feeding behavior off California, USA, with implications for prey patchiness. *Frontiers in Ecology and Evolution*. 7:338. https://doi.org/10.3389/fevo.2019.00338

---

### 5. Blue whales Eastern North Pacific 2003 (State-space model output)
**Citations:**  
Mate BR, Palacios DM, Irvine LM, Follett TM. 2019. Data from: Behavioural estimation of blue whale movements in the Northeast Pacific from state-space model analysis of satellite tracks. *Movebank Data Repository*. https://doi.org/10.5441/001/1.5ph88fk2  

Bailey H, Mate BR, Palacios DM, Irvine L, Bograd SJ, Costa DP. 2009. Behavioural estimation of blue whale movements in the Northeast Pacific from state-space model analysis of satellite tracks. *Endangered Species Research*. 10(1):93–106. https://doi.org/10.3354/esr00239  

Abrahms B et al. 2019. Memory and resource tracking drive basin-scale migrations. *Proceedings of the National Academy of Sciences USA*. 116(12):5582–5587. https://doi.org/10.1073/pnas.1819031116  

Hazen EL et al. 2016. WhaleWatch: a dynamic management tool for predicting blue whale density in the California Current. *Journal of Applied Ecology*. 54(5):1415–1428. https://doi.org/10.1111/1365-2664.12820  

Irvine LM et al. 2014. Spatial and temporal occurrence of blue whales off the U.S. west coast, with implications for management. *PLOS ONE*. 9(7):e102959. https://doi.org/10.1371/journal.pone.0102959  

Etnoyer P et al. 2006. Sea-surface temperature gradients across blue whale and sea turtle foraging trajectories off the Baja California Peninsula, Mexico. *Deep-Sea Research II*. 53(3–4):340–358. https://doi.org/10.1016/j.dsr2.2006.01.010  

Etnoyer P et al. 2004. Persistent pelagic habitats in the Baja California to Bering Sea (B2B) ecoregion. *Oceanography*. 17(1):90–101. https://doi.org/10.5670/oceanog.2004.71  

Mate BR, Lagerquist BA, Calambokidis J. 1999. Movements of North Pacific blue whales during the feeding season off southern California and their southern fall migration. *Marine Mammal Science*. 15(4):1246–1257. https://doi.org/10.1111/j.1748-7692.1999.tb00888.x

---

### 6. Blue whales Eastern North Pacific 2003 (duplicate study listing)
**Citation:**  
Bailey H, Mate BR, Palacios DM, Irvine L, Bograd SJ, Costa DP. 2009. Behavioural estimation of blue whale movements in the Northeast Pacific from state-space model analysis of satellite tracks. *Endangered Species Research*. 10(1):93–106. https://doi.org/10.3354/esr00239

---

### 7. False Killer Whales – Hawaiian Islands (PIFSC)
**Citation:**  
Study metadata reference: NOAA Fisheries, Pacific Islands Fisheries Science Center (PIFSC).  
Principal Investigator: Erin Oleson.  
Contact: NOAA Fisheries, 1845 Wasp Blvd., Bldg. 176, Honolulu, HI 96818.

---

### 8. Fin whales, Gulf of California 2001 (Argos)
**Citations:**  
Mate BR, Palacios DM, Follett TM. 2019. Data from: Fin whale movements in the Gulf of California, Mexico, from satellite telemetry. *Movebank Data Repository*. doi: 10.5441/001/1.65h5s5p2  

Jiménez-López ME, Palacios DM, Jaramillo A, Urbán J, Mate B. 2019. Fin whale movements in the Gulf of California, Mexico, from satellite telemetry. *PLOS ONE*. 14(1):e0209324. doi: 10.1371/journal.pone.0209324

---

### 9. Movements of Australia’s east coast humpback whales
**Citations:**  
Andrews-Goff V et al. 2023. Data from: Australia’s east coast humpback whales: satellite tag derived movements on breeding grounds, feeding grounds and along the northern and southern migration. *Movebank Data Repository*. https://doi.org/10.5441/001/1.294  

Andrews-Goff V et al. 2023. Australia’s east coast humpback whales: satellite tag derived movements on breeding grounds, feeding grounds and along the northern and southern migration. *Biodiversity Data Journal*. 11:e114729. https://doi.org/10.3897/BDJ.11.e114729

---

### 10. Short-finned pilot whales, NW Atlantic (CRC)
**Citation:**  
Study metadata reference. Principal Investigator: Robin W. Baird.

---

### 11. Sperm whales Gulf of California 2007–2008 (ADB tags, Argos)
**Citation:**  
Irvine L, Palacios DM, Urbán J, Mate B. 2017. Sperm whale dive behavior characteristics derived from intermediate-duration archival tag data. *Ecology and Evolution*. 7:7822–7837. doi: 10.1002/ece3.3322

---

### 12. Sperm whales Gulf of Mexico 2011–2013 (Argos)
**Citations:**  
Irvine LM, Follett TM, Winsor MH, Mate BR, Palacios DM. 2020. Data from: Sperm whales Gulf of Mexico 2011–2013 – Argos data. *Movebank Data Repository*. doi: 10.5441/001/1.tj291471  

Irvine LM, Winsor MH, Follett TM, Mate BR, Palacios DM. 2020. An at-sea assessment of Argos location accuracy for three species of large whales, and the effect of deep-diving behavior on location error. *Animal Biotelemetry*. 8:20. doi: 10.1186/s40317-020-00207-x

---

### 13. Whale shark movements in the Gulf of Mexico
**Citation:**  
Acknowledgement-based reference. Research supported by aerial search teams (On Wings of Care), volunteers from USM-GCRL, LDWF staff, colleagues from Flower Garden Banks National Marine Sanctuary, and multiple vessel captains.





