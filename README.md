# Hippocampal representations of temporal regularities increase in scale and symmetry across development
* aka temple (TEMPoral LEarning experiment)
  
---
### Highlights:
* Quantified how neural representations of temporal structure evolve across development using multivariate similarity measures
* Operationalized statistical learning as changes in representational structure before vs. after experiencing predictable continuous sequences
* Modeled learning-related neural dynamics using univariate time-series analyses and interaction-based connectivity models (PPI)
* Linked multivariate representational structure to changes in human behavior across development
* End-to-end, reproducible analysis pipeline from fMRI preprocessing through inferential statistics and figure generation

### Methods at a glance:
* Representational similarity analysis (RSA) on multivariate fMRI time series
* Pre/post learning comparisons of neural representations
* Model-based quantification of temporal scale, symmetry, and transition sensitivity
* Data-driven and ROI-based feature extraction
* Mixed-effects modeling and permutation-/simulation-based inference
* HPC-compatible, fully reproducible workflows
---

<img width="2237" height="1387" alt="Fig2_hippocampal_rsa_NEW" src="https://github.com/user-attachments/assets/dddd4282-a71a-4023-95f1-0a2d2219be3f" />
<img width="2310" height="1718" alt="Fig3_symmetry" src="https://github.com/user-attachments/assets/630b4b85-0464-4692-a97b-217cd0184d21" />

---


### Repo description: 
This repository includes end-to-end code and documentation for all analyses, from fMRI preprocessing through inferential statistics and figure generation. Anonymized, subject-level datasets derived from preprocessed fMRI data are provided, enabling full replication of all reported analyses and figures.

For step-by-step, manuscript-aligned analyses, see **[full_manuscript_analyses.md](https://github.com/owenfriend24/temple/blob/main/full_manuscript_analyses.md)** which includes embedded links to modular markdown files and Jupyter/R notebooks, as well as example function calls optimized for high-performance computing environments. 

Additional markdown files include extended analysis description and logic, but see **[main manuscript]()** for conceptual descriptions and justification of all hypotheses and analyses.

---

### Project description:
Statistical learning - the extraction of regularities from experience - is a fundamental function of the episodic memory system that supports prediction and memory-guided behavior. In adults, hippocampus supports statistical learning by integrating experiences that reliably co-occur in time, resulting in more similar neural representations for temporally linked items. Although neuroimaging work suggests that the hippocampus is also engaged during statistical learning in infants, behavioral evidence shows that the ability to learn temporal regularities improves significantly across childhood and adolescence. How the underlying neural representations which give rise to these behavioral differences change across development, however, remains untested. This study quantifies developmental differences in the neural representation of temporal regularities in children (7–9 years), early adolescents (10–12 years), and adults during a statistical learning task. 

Participants viewed implicitly structured sequences while undergoing fMRI and were later tested on memory for statistical regularities. Representational similarity during item presentations before and after learning provided direct measures of learning-related representational change. We identified three primary mechanisms underlying developmental gains in statistical learning: 1) representational scale, reflecting integration across broader temporal windows, 2) representational symmetry, reflecting bidirectional linking of sequences in forward and backward time, and 3) transition sensitivity, reflecting neural tracking of transitional probabilities and associated hippocampal–cortical interactions. We demonstrate that children show more local, forward-only representations consistent with earlier-maturing posterior hippocampal function, whereas adolescents and adults exhibit broader, bidirectional representations supported by anterior hippocampus and hippocampal–prefrontal coupling. 

By formalizing the development statistical learning as a problem of representational structure and flexibility, this study provides a mechanistic account of how neural representations of temporal structure develop and how these changes support continued improvements in  learning and memory into adulthood.

---


Feel free to reach out to corresponding author Owen Friend at ofriend@utexas.edu with any questions!
