/**
 * supplementary-tables.js
 * Interactive In-Browser Supplementary Table Explorer
 * Near-Null Magnetic Fields in Lunar Plant Biology (npj Microgravity / LSSR)
 * Supports Table S1 (80 audited papers) & Table S2 (6 public multi-omics datasets)
 */

(function () {
  "use strict";

  const TABLE_S1_DATA = [
  {
    "Reference_ID": "REF-01",
    "Citation_Number": 1,
    "Authors": "NASA",
    "Title": "NASA selects first science instruments for astronauts to deploy on Moon",
    "Journal_Or_Source": "NASA Press Release 24-046 (26 March 2024)",
    "Thematic_Category": "Planetary Magnetism & Exploration Environment",
    "DOI_Or_URL": "https://www.nasa.gov/news-release/nasa-selects-first-science-instruments-for-astronauts-to-deploy-on-moon/",
    "Year": "2024",
    "Full_Citation": "NASA. NASA selects first science instruments for astronauts to deploy on Moon. NASA Press Release 24-046 (26 March 2024). https://www.nasa.gov/news-release/nasa-selects-first-science-instruments-for-astronauts-to-deploy-on-moon/"
  },
  {
    "Reference_ID": "REF-02",
    "Citation_Number": 2,
    "Authors": "Maffei, M. E., Balestrini, R., Costantino, P. & Lanfranco, L",
    "Title": "The physiology of plants in the context of space exploration",
    "Journal_Or_Source": "Commun. Biol. 7, 1311 (2024)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1038/s42003-024-06989-7",
    "Year": "2024",
    "Full_Citation": "Maffei, M. E., Balestrini, R., Costantino, P. & Lanfranco, L. The physiology of plants in the context of space exploration. Commun. Biol. 7, 1311 (2024). https://doi.org/10.1038/s42003-024-06989-7"
  },
  {
    "Reference_ID": "REF-03",
    "Citation_Number": 3,
    "Authors": "Fountain, L. L. et al.",
    "Title": "Expanding frontiers: harnessing plant biology for space exploration and planetary sustainability",
    "Journal_Or_Source": "New Phytol. 249, 656–669 (2026)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1111/nph.70662",
    "Year": "2026",
    "Full_Citation": "Fountain, L. L. et al.. Expanding frontiers: harnessing plant biology for space exploration and planetary sustainability. New Phytol. 249, 656–669 (2026). https://doi.org/10.1111/nph.70662"
  },
  {
    "Reference_ID": "REF-04",
    "Citation_Number": 4,
    "Authors": "Wheeler, R. M",
    "Title": "Agriculture for space: People and places paving the way",
    "Journal_Or_Source": "Open Agric. 2, 14–32 (2017)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1515/opag-2017-0002",
    "Year": "2017",
    "Full_Citation": "Wheeler, R. M. Agriculture for space: People and places paving the way. Open Agric. 2, 14–32 (2017). https://doi.org/10.1515/opag-2017-0002"
  },
  {
    "Reference_ID": "REF-05",
    "Citation_Number": 5,
    "Authors": "Massa, G. D. et al.",
    "Title": "Selection of leafy green vegetable crops for a space mission",
    "Journal_Or_Source": "Gravit. Space Res. 3, 32–40 (2015)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "",
    "Year": "2015",
    "Full_Citation": "Massa, G. D. et al.. Selection of leafy green vegetable crops for a space mission. Gravit. Space Res. 3, 32–40 (2015)."
  },
  {
    "Reference_ID": "REF-06",
    "Citation_Number": 6,
    "Authors": "Space Lab Tech",
    "Title": "Lunar Effects on Agricultural Flora (LEAF) selected for Artemis missions surface deployment",
    "Journal_Or_Source": "Space Lab Technologies News (April 2024)",
    "Thematic_Category": "Planetary Magnetism & Exploration Environment",
    "DOI_Or_URL": "",
    "Year": "2024",
    "Full_Citation": "Space Lab Tech. Lunar Effects on Agricultural Flora (LEAF) selected for Artemis missions surface deployment. Space Lab Technologies News (April 2024)."
  },
  {
    "Reference_ID": "REF-07",
    "Citation_Number": 7,
    "Authors": "Paul, A.-L., Wheeler, R. M., Levine, H. G. & Ferl, R. J",
    "Title": "Fundamental plant biology in spaceflight",
    "Journal_Or_Source": "Adv. Space Res. 51, 501–510 (2013)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "https://doi.org/10.1016/j.asr.2012.09.038",
    "Year": "2013",
    "Full_Citation": "Paul, A.-L., Wheeler, R. M., Levine, H. G. & Ferl, R. J. Fundamental plant biology in spaceflight. Adv. Space Res. 51, 501–510 (2013). https://doi.org/10.1016/j.asr.2012.09.038"
  },
  {
    "Reference_ID": "REF-08",
    "Citation_Number": 8,
    "Authors": "Norcross, C. J. et al.",
    "Title": "Exploration Atmosphere: NASA’s plan for reduced pressure and elevated oxygen for future human space missions",
    "Journal_Or_Source": "48th International Conference on Environmental Systems, ICES-2018-199 (2018)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "",
    "Year": "2018",
    "Full_Citation": "Norcross, C. J. et al.. Exploration Atmosphere: NASA’s plan for reduced pressure and elevated oxygen for future human space missions. 48th International Conference on Environmental Systems, ICES-2018-199 (2018)."
  },
  {
    "Reference_ID": "REF-09",
    "Citation_Number": 9,
    "Authors": "Ferl, R. J. & Paul, A.-L",
    "Title": "The genome of Arabidopsis thaliana in spaceflight",
    "Journal_Or_Source": "Genome Biol. 17, 155 (2016)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "https://doi.org/10.1186/s13059-016-1011-3",
    "Year": "2016",
    "Full_Citation": "Ferl, R. J. & Paul, A.-L. The genome of Arabidopsis thaliana in spaceflight. Genome Biol. 17, 155 (2016). https://doi.org/10.1186/s13059-016-1011-3"
  },
  {
    "Reference_ID": "REF-10",
    "Citation_Number": 10,
    "Authors": "Sarimov, R. M., Serov, D. A. & Gudkov, S. V",
    "Title": "Hypomagnetic conditions and their biological action",
    "Journal_Or_Source": "Biology 12, 1513 (2023)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3390/biology12121513",
    "Year": "2023",
    "Full_Citation": "Sarimov, R. M., Serov, D. A. & Gudkov, S. V. Hypomagnetic conditions and their biological action. Biology 12, 1513 (2023). https://doi.org/10.3390/biology12121513"
  },
  {
    "Reference_ID": "REF-11",
    "Citation_Number": 11,
    "Authors": "Porterfield, D. M. & Barker, R. J",
    "Title": "Plant responses to near-null magnetic fields: Geomagnetism, bioenergetics, and primary metabolism in Arabidopsis and Brassica",
    "Journal_Or_Source": "Perspectives in Space Biology (in press, 2026)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2026",
    "Full_Citation": "Porterfield, D. M. & Barker, R. J. Plant responses to near-null magnetic fields: Geomagnetism, bioenergetics, and primary metabolism in Arabidopsis and Brassica. Perspectives in Space Biology (in press, 2026)."
  },
  {
    "Reference_ID": "REF-12",
    "Citation_Number": 12,
    "Authors": "Maffei, M. E",
    "Title": "Magnetic field effects on plant growth, development, and evolution",
    "Journal_Or_Source": "Front. Plant Sci. 5, 445 (2014)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3389/fpls.2014.00445",
    "Year": "2014",
    "Full_Citation": "Maffei, M. E. Magnetic field effects on plant growth, development, and evolution. Front. Plant Sci. 5, 445 (2014). https://doi.org/10.3389/fpls.2014.00445"
  },
  {
    "Reference_ID": "REF-13",
    "Citation_Number": 13,
    "Authors": "Finlay, C. C. et al.",
    "Title": "International Geomagnetic Reference Field: the thirteenth generation",
    "Journal_Or_Source": "Earth Planets Space 72, 156 (2020)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1186/s40623-020-01252-9",
    "Year": "2020",
    "Full_Citation": "Finlay, C. C. et al.. International Geomagnetic Reference Field: the thirteenth generation. Earth Planets Space 72, 156 (2020). https://doi.org/10.1186/s40623-020-01252-9"
  },
  {
    "Reference_ID": "REF-14",
    "Citation_Number": 14,
    "Authors": "Halekas, J. S. et al.",
    "Title": "Solar wind interaction with lunar crustal magnetic anomalies",
    "Journal_Or_Source": "Planet. Space Sci. 56, 941–946 (2008)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1016/j.pss.2008.01.008",
    "Year": "2008",
    "Full_Citation": "Halekas, J. S. et al.. Solar wind interaction with lunar crustal magnetic anomalies. Planet. Space Sci. 56, 941–946 (2008). https://doi.org/10.1016/j.pss.2008.01.008"
  },
  {
    "Reference_ID": "REF-15",
    "Citation_Number": 15,
    "Authors": "Borlina, C. S. et al.",
    "Title": "Re-evaluating the lunar dynamo: Constraints from Apollo sample paleomagnetism and orbital magnetic mapping",
    "Journal_Or_Source": "Earth Planet. Sci. Lett. 584, 117446 (2022)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2022",
    "Full_Citation": "Borlina, C. S. et al.. Re-evaluating the lunar dynamo: Constraints from Apollo sample paleomagnetism and orbital magnetic mapping. Earth Planet. Sci. Lett. 584, 117446 (2022)."
  },
  {
    "Reference_ID": "REF-16",
    "Citation_Number": 16,
    "Authors": "Mitchell, D. L., Halekas, J. S. & Lin, R. P",
    "Title": "Global mapping of lunar crustal magnetic fields by Lunar Prospector",
    "Journal_Or_Source": "Icarus 194, 401–409 (2008)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1016/j.icarus.2007.10.027",
    "Year": "2008",
    "Full_Citation": "Mitchell, D. L., Halekas, J. S. & Lin, R. P. Global mapping of lunar crustal magnetic fields by Lunar Prospector. Icarus 194, 401–409 (2008). https://doi.org/10.1016/j.icarus.2007.10.027"
  },
  {
    "Reference_ID": "REF-17",
    "Citation_Number": 17,
    "Authors": "Tsunakawa, H. et al.",
    "Title": "Surface vector mapping of magnetic anomalies over the Moon using Kaguya and Lunar Prospector observations",
    "Journal_Or_Source": "J. Geophys. Res. Planets 120, 1160–1185 (2015)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/2014JE004785",
    "Year": "2015",
    "Full_Citation": "Tsunakawa, H. et al.. Surface vector mapping of magnetic anomalies over the Moon using Kaguya and Lunar Prospector observations. J. Geophys. Res. Planets 120, 1160–1185 (2015). https://doi.org/10.1002/2014JE004785"
  },
  {
    "Reference_ID": "REF-18",
    "Citation_Number": 18,
    "Authors": "Hood, L. L. et al.",
    "Title": "Magnetic anomalies at the lunar South Pole: Implications for Artemis landing sites",
    "Journal_Or_Source": "J. Geophys. Res. Planets 127, e2022JE007280 (2022)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2022",
    "Full_Citation": "Hood, L. L. et al.. Magnetic anomalies at the lunar South Pole: Implications for Artemis landing sites. J. Geophys. Res. Planets 127, e2022JE007280 (2022)."
  },
  {
    "Reference_ID": "REF-19",
    "Citation_Number": 19,
    "Authors": "Hoffmann, A. P. et al.",
    "Title": "Enhancing magnetic field analysis on the KMAG instrument: applying WAIC-UP for spacecraft interference removal and interpolating data gaps",
    "Journal_Or_Source": "Earth Space Sci. 12, e2025EA004427 (2025)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1029/2025EA004427",
    "Year": "2025",
    "Full_Citation": "Hoffmann, A. P. et al.. Enhancing magnetic field analysis on the KMAG instrument: applying WAIC-UP for spacecraft interference removal and interpolating data gaps. Earth Space Sci. 12, e2025EA004427 (2025). https://doi.org/10.1029/2025EA004427"
  },
  {
    "Reference_ID": "REF-20",
    "Citation_Number": 20,
    "Authors": "Binhi, V. N. & Prato, F. S",
    "Title": "Biological effects of the hypomagnetic field: an analytical review of experiments and theories",
    "Journal_Or_Source": "PLoS ONE 12, e0179340 (2017)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1371/journal.pone.0179340",
    "Year": "2017",
    "Full_Citation": "Binhi, V. N. & Prato, F. S. Biological effects of the hypomagnetic field: an analytical review of experiments and theories. PLoS ONE 12, e0179340 (2017). https://doi.org/10.1371/journal.pone.0179340"
  },
  {
    "Reference_ID": "REF-21",
    "Citation_Number": 21,
    "Authors": "Zhang, Z. et al.",
    "Title": "Biological effects of hypomagnetic field: ground-based data for space exploration",
    "Journal_Or_Source": "Bioelectromagnetics 42, 516–531 (2021)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/bem.22360",
    "Year": "2021",
    "Full_Citation": "Zhang, Z. et al.. Biological effects of hypomagnetic field: ground-based data for space exploration. Bioelectromagnetics 42, 516–531 (2021). https://doi.org/10.1002/bem.22360"
  },
  {
    "Reference_ID": "REF-22",
    "Citation_Number": 22,
    "Authors": "Kyriacou, M. C. et al.",
    "Title": "Microgreens: Novel fresh and functional food to explore all the way from plate to space",
    "Journal_Or_Source": "Trends Food Sci. Technol. 110, 377–389 (2021)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1016/j.tifs.2021.01.080",
    "Year": "2021",
    "Full_Citation": "Kyriacou, M. C. et al.. Microgreens: Novel fresh and functional food to explore all the way from plate to space. Trends Food Sci. Technol. 110, 377–389 (2021). https://doi.org/10.1016/j.tifs.2021.01.080"
  },
  {
    "Reference_ID": "REF-23",
    "Citation_Number": 23,
    "Authors": "Bewley, J. D",
    "Title": "Seed germination and dormancy",
    "Journal_Or_Source": "Plant Cell 9, 1055–1066 (1997)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1105/tpc.9.7.1055",
    "Year": "1997",
    "Full_Citation": "Bewley, J. D. Seed germination and dormancy. Plant Cell 9, 1055–1066 (1997). https://doi.org/10.1105/tpc.9.7.1055"
  },
  {
    "Reference_ID": "REF-24",
    "Citation_Number": 24,
    "Authors": "Gommers, C. M. & Monte, E",
    "Title": "Seedling establishment: A dimmer switch-regulated process between dark and light signaling",
    "Journal_Or_Source": "Plant Physiol. 176, 1061–1074 (2017)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1104/pp.17.01460",
    "Year": "2017",
    "Full_Citation": "Gommers, C. M. & Monte, E. Seedling establishment: A dimmer switch-regulated process between dark and light signaling. Plant Physiol. 176, 1061–1074 (2017). https://doi.org/10.1104/pp.17.01460"
  },
  {
    "Reference_ID": "REF-25",
    "Citation_Number": 25,
    "Authors": "Finkelstein, R., Reeves, W., Ariizumi, T. & Steber, C",
    "Title": "Molecular aspects of seed dormancy",
    "Journal_Or_Source": "Annu. Rev. Plant Biol. 59, 387–415 (2008)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1146/annurev.arplant.59.032607.092740",
    "Year": "2008",
    "Full_Citation": "Finkelstein, R., Reeves, W., Ariizumi, T. & Steber, C. Molecular aspects of seed dormancy. Annu. Rev. Plant Biol. 59, 387–415 (2008). https://doi.org/10.1146/annurev.arplant.59.032607.092740"
  },
  {
    "Reference_ID": "REF-26",
    "Citation_Number": 26,
    "Authors": "Belyavskaya, N. A",
    "Title": "Biological effects due to weak magnetic field on plants",
    "Journal_Or_Source": "Adv. Space Res. 34, 1566–1574 (2004)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1016/j.asr.2004.01.021",
    "Year": "2004",
    "Full_Citation": "Belyavskaya, N. A. Biological effects due to weak magnetic field on plants. Adv. Space Res. 34, 1566–1574 (2004). https://doi.org/10.1016/j.asr.2004.01.021"
  },
  {
    "Reference_ID": "REF-27",
    "Citation_Number": 27,
    "Authors": "Novitskii, Y. I., Novitskaya, G. V. & Kocheshkova, T. K",
    "Title": "Growth of radish seedlings in a hypomagnetic field",
    "Journal_Or_Source": "Russ. J. Plant Physiol. 61, 667–676 (2014)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2014",
    "Full_Citation": "Novitskii, Y. I., Novitskaya, G. V. & Kocheshkova, T. K. Growth of radish seedlings in a hypomagnetic field. Russ. J. Plant Physiol. 61, 667–676 (2014)."
  },
  {
    "Reference_ID": "REF-28",
    "Citation_Number": 28,
    "Authors": "Xu, C., Wei, S. & Lü, Y",
    "Title": "Removal of the local geomagnetic field affects reproductive growth in Arabidopsis",
    "Journal_Or_Source": "Bioelectromagnetics 34, 437–442 (2013)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/bem.21788",
    "Year": "2013",
    "Full_Citation": "Xu, C., Wei, S. & Lü, Y. Removal of the local geomagnetic field affects reproductive growth in Arabidopsis. Bioelectromagnetics 34, 437–442 (2013). https://doi.org/10.1002/bem.21788"
  },
  {
    "Reference_ID": "REF-29",
    "Citation_Number": 29,
    "Authors": "Negishi, Y. et al.",
    "Title": "Growth and development of Arabidopsis thaliana under hypomagnetic conditions",
    "Journal_Or_Source": "Space Util. Res. 15, 14–17 (1999)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "1999",
    "Full_Citation": "Negishi, Y. et al.. Growth and development of Arabidopsis thaliana under hypomagnetic conditions. Space Util. Res. 15, 14–17 (1999)."
  },
  {
    "Reference_ID": "REF-30",
    "Citation_Number": 30,
    "Authors": "Kordyum, E. L. & Guikema, J. A",
    "Title": "Plants in space: Changes in the cellular and organellar architecture",
    "Journal_Or_Source": "Int. J. Astrobiol. 19, 391–406 (2020)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "",
    "Year": "2020",
    "Full_Citation": "Kordyum, E. L. & Guikema, J. A. Plants in space: Changes in the cellular and organellar architecture. Int. J. Astrobiol. 19, 391–406 (2020)."
  },
  {
    "Reference_ID": "REF-31",
    "Citation_Number": 31,
    "Authors": "Tang, J., Wu, Z., Sun, Z., Liu, H. & Liu, H",
    "Title": "Lunar magnetism impairs wheat seedling photosynthesis: a simulated environment study",
    "Journal_Or_Source": "Plant Physiol. Biochem. 216, 109156 (2024)",
    "Thematic_Category": "Planetary Magnetism & Exploration Environment",
    "DOI_Or_URL": "https://doi.org/10.1016/j.plaphy.2024.109156",
    "Year": "2024",
    "Full_Citation": "Tang, J., Wu, Z., Sun, Z., Liu, H. & Liu, H. Lunar magnetism impairs wheat seedling photosynthesis: a simulated environment study. Plant Physiol. Biochem. 216, 109156 (2024). https://doi.org/10.1016/j.plaphy.2024.109156"
  },
  {
    "Reference_ID": "REF-32",
    "Citation_Number": 32,
    "Authors": "Podleśny, J., Pietruszewski, S. & Podleśna, A",
    "Title": "Efficiency of magnetic treatment of broad bean seeds cultivated under drought conditions",
    "Journal_Or_Source": "Int. Agrophys. 19, 65–71 (2005)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2005",
    "Full_Citation": "Podleśny, J., Pietruszewski, S. & Podleśna, A. Efficiency of magnetic treatment of broad bean seeds cultivated under drought conditions. Int. Agrophys. 19, 65–71 (2005)."
  },
  {
    "Reference_ID": "REF-33",
    "Citation_Number": 33,
    "Authors": "Nonogaki, H., Bassel, G. W. & Bewley, J. D",
    "Title": "Germination—still a mystery",
    "Journal_Or_Source": "Plant Sci. 179, 574–581 (2010)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1016/j.plantsci.2010.02.010",
    "Year": "2010",
    "Full_Citation": "Nonogaki, H., Bassel, G. W. & Bewley, J. D. Germination—still a mystery. Plant Sci. 179, 574–581 (2010). https://doi.org/10.1016/j.plantsci.2010.02.010"
  },
  {
    "Reference_ID": "REF-34",
    "Citation_Number": 34,
    "Authors": "Shine, M. B. & Guruprasad, K. N",
    "Title": "Impact of pre-sowing magnetic field treatment on seed germination, seedling growth, and enzymatic antioxidant defense system in soybean",
    "Journal_Or_Source": "Physiol. Mol. Biol. Plants 18, 325–334 (2012)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2012",
    "Full_Citation": "Shine, M. B. & Guruprasad, K. N. Impact of pre-sowing magnetic field treatment on seed germination, seedling growth, and enzymatic antioxidant defense system in soybean. Physiol. Mol. Biol. Plants 18, 325–334 (2012)."
  },
  {
    "Reference_ID": "REF-35",
    "Citation_Number": 35,
    "Authors": "Xu, C., Yu, Y., Zhang, Y., Li, Y. & Wei, S",
    "Title": "Gibberellins are involved in effect of near-null magnetic field on Arabidopsis flowering",
    "Journal_Or_Source": "Bioelectromagnetics 38, 1–10 (2017)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/bem.22004",
    "Year": "2017",
    "Full_Citation": "Xu, C., Yu, Y., Zhang, Y., Li, Y. & Wei, S. Gibberellins are involved in effect of near-null magnetic field on Arabidopsis flowering. Bioelectromagnetics 38, 1–10 (2017). https://doi.org/10.1002/bem.22004"
  },
  {
    "Reference_ID": "REF-36",
    "Citation_Number": 36,
    "Authors": "Xu, C., Zhang, Y., Yu, Y., Li, Y. & Wei, S",
    "Title": "Suppression of Arabidopsis flowering by near-null magnetic field is mediated by auxin",
    "Journal_Or_Source": "Bioelectromagnetics 39, 15–24 (2018)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/bem.22086",
    "Year": "2018",
    "Full_Citation": "Xu, C., Zhang, Y., Yu, Y., Li, Y. & Wei, S. Suppression of Arabidopsis flowering by near-null magnetic field is mediated by auxin. Bioelectromagnetics 39, 15–24 (2018). https://doi.org/10.1002/bem.22086"
  },
  {
    "Reference_ID": "REF-37",
    "Citation_Number": 37,
    "Authors": "Narayana, R. et al.",
    "Title": "Near-null magnetic field alters root growth and PIN2 polar auxin transporter distribution in Arabidopsis thaliana",
    "Journal_Or_Source": "Bioelectromagnetics 39, 361–374 (2018)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2018",
    "Full_Citation": "Narayana, R. et al.. Near-null magnetic field alters root growth and PIN2 polar auxin transporter distribution in Arabidopsis thaliana. Bioelectromagnetics 39, 361–374 (2018)."
  },
  {
    "Reference_ID": "REF-38",
    "Citation_Number": 38,
    "Authors": "Belyavskaya, N. A",
    "Title": "Ultrastructure of meristematic cells of pea roots grown in a hypomagnetic field",
    "Journal_Or_Source": "Biophysics 46, 953–958 (2001)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2001",
    "Full_Citation": "Belyavskaya, N. A. Ultrastructure of meristematic cells of pea roots grown in a hypomagnetic field. Biophysics 46, 953–958 (2001)."
  },
  {
    "Reference_ID": "REF-39",
    "Citation_Number": 39,
    "Authors": "Fiorillo, A. et al.",
    "Title": "14-3-3 proteins and the plasma membrane $\\text{H}^+$-ATPase are involved in maize magnetic induction",
    "Journal_Or_Source": "Plants 12, 2887 (2023)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3390/plants12152887",
    "Year": "2023",
    "Full_Citation": "Fiorillo, A. et al.. 14-3-3 proteins and the plasma membrane $\\text{H}^+$-ATPase are involved in maize magnetic induction. Plants 12, 2887 (2023). https://doi.org/10.3390/plants12152887"
  },
  {
    "Reference_ID": "REF-40",
    "Citation_Number": 40,
    "Authors": "Wheeler, R. M",
    "Title": "Carbon dioxide effects on plants: Implications for space exploration",
    "Journal_Or_Source": "Front. Astron. Space Sci. 8, 780074 (2021)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.3389/fspas.2021.780074",
    "Year": "2021",
    "Full_Citation": "Wheeler, R. M. Carbon dioxide effects on plants: Implications for space exploration. Front. Astron. Space Sci. 8, 780074 (2021). https://doi.org/10.3389/fspas.2021.780074"
  },
  {
    "Reference_ID": "REF-41",
    "Citation_Number": 41,
    "Authors": "Douglas, G. L. et al.",
    "Title": "Nutrition and food systems for exploration missions",
    "Journal_Or_Source": "NASA Human Research Program Technical Report (2020)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "",
    "Year": "2020",
    "Full_Citation": "Douglas, G. L. et al.. Nutrition and food systems for exploration missions. NASA Human Research Program Technical Report (2020)."
  },
  {
    "Reference_ID": "REF-42",
    "Citation_Number": 42,
    "Authors": "Solymosi, K. & Schoefs, B",
    "Title": "Etioplast and etio-chloroplast formation under natural and laboratory conditions",
    "Journal_Or_Source": "Front. Plant Sci. 9, 1709 (2018)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.3389/fpls.2018.01709",
    "Year": "2018",
    "Full_Citation": "Solymosi, K. & Schoefs, B. Etioplast and etio-chloroplast formation under natural and laboratory conditions. Front. Plant Sci. 9, 1709 (2018). https://doi.org/10.3389/fpls.2018.01709"
  },
  {
    "Reference_ID": "REF-43",
    "Citation_Number": 43,
    "Authors": "Tanaka, R. & Tanaka, A",
    "Title": "Tetrapyrrole biosynthesis in higher plants",
    "Journal_Or_Source": "Annu. Rev. Plant Biol. 58, 321–346 (2007)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1146/annurev.arplant.57.032905.105448",
    "Year": "2007",
    "Full_Citation": "Tanaka, R. & Tanaka, A. Tetrapyrrole biosynthesis in higher plants. Annu. Rev. Plant Biol. 58, 321–346 (2007). https://doi.org/10.1146/annurev.arplant.57.032905.105448"
  },
  {
    "Reference_ID": "REF-44",
    "Citation_Number": 44,
    "Authors": "Parmagnani, A. S. et al.",
    "Title": "The geomagnetic field is required for Lima bean photosynthesis and reactive oxygen species production",
    "Journal_Or_Source": "Int. J. Mol. Sci. 24, 2896 (2023)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3390/ijms24032896",
    "Year": "2023",
    "Full_Citation": "Parmagnani, A. S. et al.. The geomagnetic field is required for Lima bean photosynthesis and reactive oxygen species production. Int. J. Mol. Sci. 24, 2896 (2023). https://doi.org/10.3390/ijms24032896"
  },
  {
    "Reference_ID": "REF-45",
    "Citation_Number": 45,
    "Authors": "Agliassa, C. et al.",
    "Title": "Reduction of the geomagnetic field delays Arabidopsis thaliana flowering time through downregulation of flowering-related genes",
    "Journal_Or_Source": "Bioelectromagnetics 39, 361–374 (2018)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1002/bem.22123",
    "Year": "2018",
    "Full_Citation": "Agliassa, C. et al.. Reduction of the geomagnetic field delays Arabidopsis thaliana flowering time through downregulation of flowering-related genes. Bioelectromagnetics 39, 361–374 (2018). https://doi.org/10.1002/bem.22123"
  },
  {
    "Reference_ID": "REF-46",
    "Citation_Number": 46,
    "Authors": "Maffei, M. E. et al.",
    "Title": "Peppermint (Mentha $\\times$ piperita) response to near-null magnetic field involves modulated monoterpene and flavonoid biosynthesis",
    "Journal_Or_Source": "J. Plant Res. 134, 823–834 (2021)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2021",
    "Full_Citation": "Maffei, M. E. et al.. Peppermint (Mentha $\\times$ piperita) response to near-null magnetic field involves modulated monoterpene and flavonoid biosynthesis. J. Plant Res. 134, 823–834 (2021)."
  },
  {
    "Reference_ID": "REF-47",
    "Citation_Number": 47,
    "Authors": "Gangappa, S. N. & Botto, J. F",
    "Title": "The multifaceted roles of HY5 in plant growth and development",
    "Journal_Or_Source": "Mol. Plant 9, 1353–1365 (2016)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1016/j.molp.2016.07.002",
    "Year": "2016",
    "Full_Citation": "Gangappa, S. N. & Botto, J. F. The multifaceted roles of HY5 in plant growth and development. Mol. Plant 9, 1353–1365 (2016). https://doi.org/10.1016/j.molp.2016.07.002"
  },
  {
    "Reference_ID": "REF-48",
    "Citation_Number": 48,
    "Authors": "Toledo-Ortiz, G. et al.",
    "Title": "The HY5 transcription factor integrates blue-light and hormonal cues to drive plastid development",
    "Journal_Or_Source": "Plant Cell 26, 1392–1407 (2014)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "",
    "Year": "2014",
    "Full_Citation": "Toledo-Ortiz, G. et al.. The HY5 transcription factor integrates blue-light and hormonal cues to drive plastid development. Plant Cell 26, 1392–1407 (2014)."
  },
  {
    "Reference_ID": "REF-49",
    "Citation_Number": 49,
    "Authors": "Hore, P. J. & Mouritsen, H",
    "Title": "The radical-pair mechanism of magnetoreception",
    "Journal_Or_Source": "Annu. Rev. Biophys. 45, 299–344 (2016)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1146/annurev-biophys-032116-094545",
    "Year": "2016",
    "Full_Citation": "Hore, P. J. & Mouritsen, H. The radical-pair mechanism of magnetoreception. Annu. Rev. Biophys. 45, 299–344 (2016). https://doi.org/10.1146/annurev-biophys-032116-094545"
  },
  {
    "Reference_ID": "REF-50",
    "Citation_Number": 50,
    "Authors": "Solov’yov, I. A., Chandler, D. E. & Schulten, K",
    "Title": "Magnetic field effects in Arabidopsis thaliana cryptochrome-1",
    "Journal_Or_Source": "Biophys. J. 92, 2711–2726 (2007)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1529/biophysj.106.097139",
    "Year": "2007",
    "Full_Citation": "Solov’yov, I. A., Chandler, D. E. & Schulten, K. Magnetic field effects in Arabidopsis thaliana cryptochrome-1. Biophys. J. 92, 2711–2726 (2007). https://doi.org/10.1529/biophysj.106.097139"
  },
  {
    "Reference_ID": "REF-51",
    "Citation_Number": 51,
    "Authors": "Ahmad, M., Galland, P., Ritz, T., Wiltschko, R. & Wiltschko, W",
    "Title": "Magnetic intensity affects cryptochrome-dependent responses in Arabidopsis thaliana",
    "Journal_Or_Source": "Planta 225, 615–624 (2007)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1007/s00425-006-0383-0",
    "Year": "2007",
    "Full_Citation": "Ahmad, M., Galland, P., Ritz, T., Wiltschko, R. & Wiltschko, W. Magnetic intensity affects cryptochrome-dependent responses in Arabidopsis thaliana. Planta 225, 615–624 (2007). https://doi.org/10.1007/s00425-006-0383-0"
  },
  {
    "Reference_ID": "REF-52",
    "Citation_Number": 52,
    "Authors": "Briat, J.-F., Duc, C., Ravet, K. & Gaymard, F",
    "Title": "Ferritins and iron storage in plants",
    "Journal_Or_Source": "Biochim. Biophys. Acta 1800, 806–814 (2010)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1016/j.bbagen.2009.12.003",
    "Year": "2010",
    "Full_Citation": "Briat, J.-F., Duc, C., Ravet, K. & Gaymard, F. Ferritins and iron storage in plants. Biochim. Biophys. Acta 1800, 806–814 (2010). https://doi.org/10.1016/j.bbagen.2009.12.003"
  },
  {
    "Reference_ID": "REF-53",
    "Citation_Number": 53,
    "Authors": "Islam, M., Maffei, M. E. & Vigani, G",
    "Title": "The geomagnetic field is a contributing factor for an efficient iron uptake in Arabidopsis thaliana",
    "Journal_Or_Source": "Front. Plant Sci. 11, 325 (2020)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3389/fpls.2020.00325",
    "Year": "2020",
    "Full_Citation": "Islam, M., Maffei, M. E. & Vigani, G. The geomagnetic field is a contributing factor for an efficient iron uptake in Arabidopsis thaliana. Front. Plant Sci. 11, 325 (2020). https://doi.org/10.3389/fpls.2020.00325"
  },
  {
    "Reference_ID": "REF-54",
    "Citation_Number": 54,
    "Authors": "Islam, M., Vigani, G. & Maffei, M. E",
    "Title": "The geomagnetic field modulates nutrient status and lipid metabolism during Arabidopsis thaliana plant development",
    "Journal_Or_Source": "Plants 9, 1729 (2020)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3390/plants9121729",
    "Year": "2020",
    "Full_Citation": "Islam, M., Vigani, G. & Maffei, M. E. The geomagnetic field modulates nutrient status and lipid metabolism during Arabidopsis thaliana plant development. Plants 9, 1729 (2020). https://doi.org/10.3390/plants9121729"
  },
  {
    "Reference_ID": "REF-55",
    "Citation_Number": 55,
    "Authors": "Barker, R. J. & Porterfield, D. M",
    "Title": "Quantum Biology Atlas: A cross-species ontology, pathway compiler, and multi-omics projection toolkit for quantum biological mechanisms",
    "Journal_Or_Source": "Zenodo / GitHub (2026)",
    "Thematic_Category": "Mitochondrial Bioenergetics & Cellular Stress",
    "DOI_Or_URL": "https://github.com/dr-richard-barker/quantum-biology-atlas",
    "Year": "2026",
    "Full_Citation": "Barker, R. J. & Porterfield, D. M. Quantum Biology Atlas: A cross-species ontology, pathway compiler, and multi-omics projection toolkit for quantum biological mechanisms. Zenodo / GitHub (2026). https://github.com/dr-richard-barker/quantum-biology-atlas"
  },
  {
    "Reference_ID": "REF-56",
    "Citation_Number": 56,
    "Authors": "Meyer, E. H., Welchen, E. & Carrie, C",
    "Title": "Assembly of the complexes of the oxidative phosphorylation system in plant mitochondria",
    "Journal_Or_Source": "Physiol. Plant. 157, 294–309 (2016)",
    "Thematic_Category": "Mitochondrial Bioenergetics & Cellular Stress",
    "DOI_Or_URL": "",
    "Year": "2016",
    "Full_Citation": "Meyer, E. H., Welchen, E. & Carrie, C. Assembly of the complexes of the oxidative phosphorylation system in plant mitochondria. Physiol. Plant. 157, 294–309 (2016)."
  },
  {
    "Reference_ID": "REF-57",
    "Citation_Number": 57,
    "Authors": "Maeda, K. et al.",
    "Title": "Chemical compass model of avian magnetoreception",
    "Journal_Or_Source": "Nature 453, 387–390 (2008)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1038/nature06834",
    "Year": "2008",
    "Full_Citation": "Maeda, K. et al.. Chemical compass model of avian magnetoreception. Nature 453, 387–390 (2008). https://doi.org/10.1038/nature06834"
  },
  {
    "Reference_ID": "REF-58",
    "Citation_Number": 58,
    "Authors": "Pooam, M. et al.",
    "Title": "Magnetic sensitivity mediated by the Arabidopsis blue-light receptor cryptochrome occurs during flavin reoxidation in the dark",
    "Journal_Or_Source": "Planta 249, 319–332 (2019)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1007/s00425-018-3002-y",
    "Year": "2019",
    "Full_Citation": "Pooam, M. et al.. Magnetic sensitivity mediated by the Arabidopsis blue-light receptor cryptochrome occurs during flavin reoxidation in the dark. Planta 249, 319–332 (2019). https://doi.org/10.1007/s00425-018-3002-y"
  },
  {
    "Reference_ID": "REF-59",
    "Citation_Number": 59,
    "Authors": "Demmig-Adams, B. & Adams, W. W",
    "Title": "Photoprotection in an ecological context: the remarkable diversity of extreme-energy dissipation mechanisms",
    "Journal_Or_Source": "Funct. Plant Biol. 45, 697–711 (2018)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "",
    "Year": "2018",
    "Full_Citation": "Demmig-Adams, B. & Adams, W. W. Photoprotection in an ecological context: the remarkable diversity of extreme-energy dissipation mechanisms. Funct. Plant Biol. 45, 697–711 (2018)."
  },
  {
    "Reference_ID": "REF-60",
    "Citation_Number": 60,
    "Authors": "Vanlerberghe, G. C",
    "Title": "Alternative Oxidase: A mitochondrial respiratory pathway to maintain metabolic and signaling homeostasis during abiotic and biotic stress in plants",
    "Journal_Or_Source": "Int. J. Mol. Sci. 14, 6805–6847 (2013)",
    "Thematic_Category": "Mitochondrial Bioenergetics & Cellular Stress",
    "DOI_Or_URL": "https://doi.org/10.3390/ijms14046805",
    "Year": "2013",
    "Full_Citation": "Vanlerberghe, G. C. Alternative Oxidase: A mitochondrial respiratory pathway to maintain metabolic and signaling homeostasis during abiotic and biotic stress in plants. Int. J. Mol. Sci. 14, 6805–6847 (2013). https://doi.org/10.3390/ijms14046805"
  },
  {
    "Reference_ID": "REF-61",
    "Citation_Number": 61,
    "Authors": "Zadeh-Haghighi, H. & Simon, C",
    "Title": "Magnetic field effects in biology from the perspective of the radical pair mechanism",
    "Journal_Or_Source": "J. R. Soc. Interface 19, 20220325 (2022)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1098/rsif.2022.0325",
    "Year": "2022",
    "Full_Citation": "Zadeh-Haghighi, H. & Simon, C. Magnetic field effects in biology from the perspective of the radical pair mechanism. J. R. Soc. Interface 19, 20220325 (2022). https://doi.org/10.1098/rsif.2022.0325"
  },
  {
    "Reference_ID": "REF-62",
    "Citation_Number": 62,
    "Authors": "Miloslavina, Y. et al.",
    "Title": "Charge separation kinetics in intact photosystem II core particles is trap-limited: a picosecond fluorescence study",
    "Journal_Or_Source": "Biochemistry 45, 2436–2442 (2006)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1021/bi052248c",
    "Year": "2006",
    "Full_Citation": "Miloslavina, Y. et al.. Charge separation kinetics in intact photosystem II core particles is trap-limited: a picosecond fluorescence study. Biochemistry 45, 2436–2442 (2006). https://doi.org/10.1021/bi052248c"
  },
  {
    "Reference_ID": "REF-63",
    "Citation_Number": 63,
    "Authors": "Vass, I",
    "Title": "Role of charge recombination processes in photodamage and photoprotection of the photosystem II complex",
    "Journal_Or_Source": "Physiol. Plant. 142, 6–16 (2011)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1111/j.1399-3054.2011.01454.x",
    "Year": "2011",
    "Full_Citation": "Vass, I. Role of charge recombination processes in photodamage and photoprotection of the photosystem II complex. Physiol. Plant. 142, 6–16 (2011). https://doi.org/10.1111/j.1399-3054.2011.01454.x"
  },
  {
    "Reference_ID": "REF-64",
    "Citation_Number": 64,
    "Authors": "Sarewicz, M. et al.",
    "Title": "Triplet state of the semiquinone-Rieske cluster as an intermediate of electronic bifurcation catalyzed by cytochrome $bc_1$",
    "Journal_Or_Source": "Biochemistry 52, 6388–6395 (2013)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1021/bi400624m",
    "Year": "2013",
    "Full_Citation": "Sarewicz, M. et al.. Triplet state of the semiquinone-Rieske cluster as an intermediate of electronic bifurcation catalyzed by cytochrome $bc_1$. Biochemistry 52, 6388–6395 (2013). https://doi.org/10.1021/bi400624m"
  },
  {
    "Reference_ID": "REF-65",
    "Citation_Number": 65,
    "Authors": "Bujnowicz, Ł. et al.",
    "Title": "Suppression of superoxide production by a spin-spin coupling between semiquinone and the Rieske cluster in cytochrome $bc_1$",
    "Journal_Or_Source": "FEBS Lett. 593, 3–12 (2019)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1002/1873-3468.13296",
    "Year": "2019",
    "Full_Citation": "Bujnowicz, Ł. et al.. Suppression of superoxide production by a spin-spin coupling between semiquinone and the Rieske cluster in cytochrome $bc_1$. FEBS Lett. 593, 3–12 (2019). https://doi.org/10.1002/1873-3468.13296"
  },
  {
    "Reference_ID": "REF-66",
    "Citation_Number": 66,
    "Authors": "Richards, J. T. et al.",
    "Title": "Hypobaric plant growth in spaceflight: Design, gas diffusion, and physiological adaptation",
    "Journal_Or_Source": "Gravit. Space Biol. Bull. 19, 101–114 (2006)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "",
    "Year": "2006",
    "Full_Citation": "Richards, J. T. et al.. Hypobaric plant growth in spaceflight: Design, gas diffusion, and physiological adaptation. Gravit. Space Biol. Bull. 19, 101–114 (2006)."
  },
  {
    "Reference_ID": "REF-67",
    "Citation_Number": 67,
    "Authors": "da Silveira, W. A. et al.",
    "Title": "Comprehensive multi-omics analysis reveals mitochondrial stress as a central biological hub for spaceflight impact",
    "Journal_Or_Source": "Cell 183, 1185–1201 (2020)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "https://doi.org/10.1016/j.cell.2020.11.002",
    "Year": "2020",
    "Full_Citation": "da Silveira, W. A. et al.. Comprehensive multi-omics analysis reveals mitochondrial stress as a central biological hub for spaceflight impact. Cell 183, 1185–1201 (2020). https://doi.org/10.1016/j.cell.2020.11.002"
  },
  {
    "Reference_ID": "REF-68",
    "Citation_Number": 68,
    "Authors": "Bauwe, H., Hagemann, M. & Fernie, A. R",
    "Title": "Photorespiration: players, partners and origin",
    "Journal_Or_Source": "Trends Plant Sci. 15, 330–336 (2010)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://doi.org/10.1016/j.tplants.2010.03.006",
    "Year": "2010",
    "Full_Citation": "Bauwe, H., Hagemann, M. & Fernie, A. R. Photorespiration: players, partners and origin. Trends Plant Sci. 15, 330–336 (2010). https://doi.org/10.1016/j.tplants.2010.03.006"
  },
  {
    "Reference_ID": "REF-69",
    "Citation_Number": 69,
    "Authors": "Moore, A. L. & Siedow, J. N",
    "Title": "The regulation and nature of the cyanide-resistant alternative oxidase of plant mitochondria",
    "Journal_Or_Source": "Biochim. Biophys. Acta 1059, 121–140 (1991)",
    "Thematic_Category": "Mitochondrial Bioenergetics & Cellular Stress",
    "DOI_Or_URL": "",
    "Year": "1991",
    "Full_Citation": "Moore, A. L. & Siedow, J. N. The regulation and nature of the cyanide-resistant alternative oxidase of plant mitochondria. Biochim. Biophys. Acta 1059, 121–140 (1991)."
  },
  {
    "Reference_ID": "REF-70",
    "Citation_Number": 70,
    "Authors": "Maxwell, D. P., Wang, Y. & McIntosh, L",
    "Title": "The alternative oxidase lowers mitochondrial reactive oxygen production in plant cells",
    "Journal_Or_Source": "Proc. Natl. Acad. Sci. USA 96, 8271–8276 (1999)",
    "Thematic_Category": "Mitochondrial Bioenergetics & Cellular Stress",
    "DOI_Or_URL": "https://doi.org/10.1073/pnas.96.14.8271",
    "Year": "1999",
    "Full_Citation": "Maxwell, D. P., Wang, Y. & McIntosh, L. The alternative oxidase lowers mitochondrial reactive oxygen production in plant cells. Proc. Natl. Acad. Sci. USA 96, 8271–8276 (1999). https://doi.org/10.1073/pnas.96.14.8271"
  },
  {
    "Reference_ID": "REF-71",
    "Citation_Number": 71,
    "Authors": "Arena, C. et al.",
    "Title": "Plants in space: Responses to ionizing radiation and interaction with microgravity",
    "Journal_Or_Source": "Front. Plant Sci. 5, 550 (2014)",
    "Thematic_Category": "Space Radiation & Multi-Stressor Synergy",
    "DOI_Or_URL": "https://doi.org/10.3389/fpls.2014.00550",
    "Year": "2014",
    "Full_Citation": "Arena, C. et al.. Plants in space: Responses to ionizing radiation and interaction with microgravity. Front. Plant Sci. 5, 550 (2014). https://doi.org/10.3389/fpls.2014.00550"
  },
  {
    "Reference_ID": "REF-72",
    "Citation_Number": 72,
    "Authors": "Cucinotta, F. A. & Durante, M",
    "Title": "Cancer risk from exposure to galactic cosmic rays: implications for early exploration missions",
    "Journal_Or_Source": "Lancet Oncol. 7, 431–435 (2006)",
    "Thematic_Category": "Space Radiation & Multi-Stressor Synergy",
    "DOI_Or_URL": "",
    "Year": "2006",
    "Full_Citation": "Cucinotta, F. A. & Durante, M. Cancer risk from exposure to galactic cosmic rays: implications for early exploration missions. Lancet Oncol. 7, 431–435 (2006)."
  },
  {
    "Reference_ID": "REF-73",
    "Citation_Number": 73,
    "Authors": "Parmagnani, A. S., Mannino, G. & Maffei, M. E",
    "Title": "Transcriptomics and metabolomics of reactive oxygen species modulation in near-null magnetic field-induced Arabidopsis thaliana",
    "Journal_Or_Source": "Biomolecules 12, 1824 (2022)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.3390/biom12121824",
    "Year": "2022",
    "Full_Citation": "Parmagnani, A. S., Mannino, G. & Maffei, M. E. Transcriptomics and metabolomics of reactive oxygen species modulation in near-null magnetic field-induced Arabidopsis thaliana. Biomolecules 12, 1824 (2022). https://doi.org/10.3390/biom12121824"
  },
  {
    "Reference_ID": "REF-74",
    "Citation_Number": 74,
    "Authors": "Garrett-Bakelman, F. E. et al.",
    "Title": "The NASA Twins Study: A multidimensional analysis of a year-long human spaceflight",
    "Journal_Or_Source": "Science 364, eaau8650 (2019)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "https://doi.org/10.1126/science.aau8650",
    "Year": "2019",
    "Full_Citation": "Garrett-Bakelman, F. E. et al.. The NASA Twins Study: A multidimensional analysis of a year-long human spaceflight. Science 364, eaau8650 (2019). https://doi.org/10.1126/science.aau8650"
  },
  {
    "Reference_ID": "REF-75",
    "Citation_Number": 75,
    "Authors": "Barker, R. J. et al.",
    "Title": "Spaceflight-induced changes in gene expression, chromatin accessibility, and histone modifications across Arabidopsis thaliana ecotypes",
    "Journal_Or_Source": "NPJ Microgravity 9, 42 (2023)",
    "Thematic_Category": "Spaceflight Plant Physiology & BLSS",
    "DOI_Or_URL": "https://doi.org/10.1038/s41526-023-00287-2",
    "Year": "2023",
    "Full_Citation": "Barker, R. J. et al.. Spaceflight-induced changes in gene expression, chromatin accessibility, and histone modifications across Arabidopsis thaliana ecotypes. NPJ Microgravity 9, 42 (2023). https://doi.org/10.1038/s41526-023-00287-2"
  },
  {
    "Reference_ID": "REF-76",
    "Citation_Number": 76,
    "Authors": "Mo, W. C. et al.",
    "Title": "Hypomagnetic field alters human neuroblastoma cell cycle kinetics and transcriptomic networks",
    "Journal_Or_Source": "PLoS ONE 7, e44650 (2012)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2012",
    "Full_Citation": "Mo, W. C. et al.. Hypomagnetic field alters human neuroblastoma cell cycle kinetics and transcriptomic networks. PLoS ONE 7, e44650 (2012)."
  },
  {
    "Reference_ID": "REF-77",
    "Citation_Number": 77,
    "Authors": "Xu, C. et al.",
    "Title": "Hypomagnetic field promotes osteoclastogenesis and suppresses osteoblastogenesis in rat bone marrow cell cultures",
    "Journal_Or_Source": "Bioelectromagnetics 33, 685–694 (2012)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "",
    "Year": "2012",
    "Full_Citation": "Xu, C. et al.. Hypomagnetic field promotes osteoclastogenesis and suppresses osteoblastogenesis in rat bone marrow cell cultures. Bioelectromagnetics 33, 685–694 (2012)."
  },
  {
    "Reference_ID": "REF-78",
    "Citation_Number": 78,
    "Authors": "Harris, S.-R. et al.",
    "Title": "Effect of magnetic fields on cryptochrome-dependent responses in Arabidopsis thaliana",
    "Journal_Or_Source": "J. R. Soc. Interface 6, 1193–1205 (2009)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1098/rsif.2008.0519",
    "Year": "2009",
    "Full_Citation": "Harris, S.-R. et al.. Effect of magnetic fields on cryptochrome-dependent responses in Arabidopsis thaliana. J. R. Soc. Interface 6, 1193–1205 (2009). https://doi.org/10.1098/rsif.2008.0519"
  },
  {
    "Reference_ID": "REF-79",
    "Citation_Number": 79,
    "Authors": "Albaqami, M. et al.",
    "Title": "Arabidopsis cryptochrome is responsive to radiofrequency electromagnetic fields",
    "Journal_Or_Source": "Sci. Rep. 10, 11260 (2020)",
    "Thematic_Category": "Hypomagnetic Biology & Quantum Biophysics",
    "DOI_Or_URL": "https://doi.org/10.1038/s41598-020-67165-5",
    "Year": "2020",
    "Full_Citation": "Albaqami, M. et al.. Arabidopsis cryptochrome is responsive to radiofrequency electromagnetic fields. Sci. Rep. 10, 11260 (2020). https://doi.org/10.1038/s41598-020-67165-5"
  },
  {
    "Reference_ID": "REF-80",
    "Citation_Number": 80,
    "Authors": "Williams, P. H",
    "Title": "Rapid-cycling Brassica species in laboratory research and education. In: Tested Studies for Laboratory Teaching (ed. C. A. Goldman), Proceedings of the 10th Workshop/Conference of the Association for Biology Laboratory Education (ABLE), Vol. 10, pp",
    "Journal_Or_Source": "1–16 (1989)",
    "Thematic_Category": "Plant Growth & Photomorphogenesis",
    "DOI_Or_URL": "https://www.ableweb.org/biologylabs/wp-content/uploads/volumes/vol-10/1-williams.pdf",
    "Year": "1989",
    "Full_Citation": "Williams, P. H. Rapid-cycling Brassica species in laboratory research and education. In: Tested Studies for Laboratory Teaching (ed. C. A. Goldman), Proceedings of the 10th Workshop/Conference of the Association for Biology Laboratory Education (ABLE), Vol. 10, pp. 1–16 (1989). https://www.ableweb.org/biologylabs/wp-content/uploads/volumes/vol-10/1-williams.pdf"
  }
];
  const TABLE_S2_DATA = [
  {
    "Dataset_ID": "DS-01",
    "Repository": "NASA Open Science Data Repository (OSDR)",
    "Accession": "OSD-782",
    "Target_System": "Arabidopsis thaliana (Seedling multi-omics)",
    "Platform_Or_Mission": "Spaceflight / Ground multi-stressor analog",
    "Assay_Types": "RNA-seq Transcriptomics & Metabolomics",
    "Description": "Seedling transcriptomic and metabolomic response to exploration atmosphere (elevated CO2, 34% O2, hypobaric pressure) and simulated radiation.",
    "DOI_Or_URL": "https://doi.org/10.26030/osd-782"
  },
  {
    "Dataset_ID": "DS-02",
    "Repository": "NASA Open Science Data Repository (OSDR)",
    "Accession": "OSD-8",
    "Target_System": "Arabidopsis thaliana (EMCS spaceflight seedling growth)",
    "Platform_Or_Mission": "International Space Station (European Modular Cultivation System)",
    "Assay_Types": "Microarray Transcriptomics & Growth Morphometry",
    "Description": "Microgravity and fractional-g seedling development, blue-light phototropism, and gene expression during early autotrophic establishment.",
    "DOI_Or_URL": "https://doi.org/10.26030/osd-8"
  },
  {
    "Dataset_ID": "DS-03",
    "Repository": "NASA Open Science Data Repository (OSDR)",
    "Accession": "OSD-27",
    "Target_System": "Arabidopsis thaliana (BRIC-16 Spaceflight Experiment)",
    "Platform_Or_Mission": "Space Shuttle STS-131 (Biological Research in Canisters)",
    "Assay_Types": "Proteomics & Transcriptomics",
    "Description": "Dark-grown etiolated seedling proteome and transcriptome during germination and radicle emergence in spaceflight.",
    "DOI_Or_URL": "https://doi.org/10.26030/osd-27"
  },
  {
    "Dataset_ID": "DS-04",
    "Repository": "NASA Planetary Data System (PDS) / JAXA SELENE Data Archive",
    "Accession": "LP-MAG / KAGUYA-MAP-LMAG",
    "Target_System": "Moon Global Crustal Magnetic Field (30 km & surface grid)",
    "Platform_Or_Mission": "Lunar Prospector & Kaguya (SELENE) Lunar Orbiters",
    "Assay_Types": "Vector Magnetometer Field Surveys (Bx, By, Bz, |B|)",
    "Description": "High-resolution orbital magnetometer vector datasets and spherical harmonic crustal paleomagnetic field models across 23 candidate and historical landing sites.",
    "DOI_Or_URL": "https://doi.org/10.17189/rk57-g992"
  },
  {
    "Dataset_ID": "DS-05",
    "Repository": "Quantum Biology Atlas / Systems Biology Graphical Notation (SBGN)",
    "Accession": "QBM-06",
    "Target_System": "Cryptochrome & Organellar Radical Pair Biochemical Networks",
    "Platform_Or_Mission": "Computational Systems Biology Model",
    "Assay_Types": "Biophysical Spin Kinetics & Kinetic Rate Models",
    "Description": "Standardized pathway architecture for heterotrophic seed germination, flavin-tryptophan radical pairs, HY5 transcriptional activation, and mitochondrial electron transport.",
    "DOI_Or_URL": "https://github.com/dr-richard-barker/NMF_review/tree/main/data"
  },
  {
    "Dataset_ID": "DS-06",
    "Repository": "Cell Spaceflight Astronaut Multi-Omics Consortium",
    "Accession": "Afshinnekoo et al. (2020) Dataset",
    "Target_System": "Homo sapiens (Astronaut peripheral blood mononuclear cells & plasma)",
    "Platform_Or_Mission": "NASA Twins Study / ISS Long-Duration Expeditions",
    "Assay_Types": "Multi-Omics (RNA-seq, Proteomics, Metabolomics, Cell-Free DNA)",
    "Description": "Conserved core mitochondrial dysregulation, oxidative phosphorylation stress, and systemic cell-free mitochondrial DNA leakage in astronauts during spaceflight.",
    "DOI_Or_URL": "https://doi.org/10.1016/j.cell.2020.11.002"
  }
];

  // State Management
  const state = {
    activeTab: "s1", // "s1" | "s2"
    searchQuery: "",
    categoryFilter: "All",
    sortColumn: "Citation_Number",
    sortAsc: true,
    currentPage: 1,
    pageSize: 10,
    s2View: "cards" // "cards" | "table"
  };

  function getCategoryBadgeClass(category) {
    switch (category) {
      case "Hypomagnetic Biology & Quantum Biophysics":
        return "cat-purple";
      case "Plant Growth & Photomorphogenesis":
        return "cat-green";
      case "Spaceflight Plant Physiology & BLSS":
        return "cat-blue";
      case "Mitochondrial Bioenergetics & Cellular Stress":
        return "cat-amber";
      case "Planetary Magnetism & Exploration Environment":
        return "cat-cyan";
      case "Space Radiation & Multi-Stressor Synergy":
        return "cat-rose";
      default:
        return "cat-default";
    }
  }

  function getRepositoryBadgeClass(repo) {
    if (repo.includes("OSDR")) return "repo-osdr";
    if (repo.includes("PDS") || repo.includes("JAXA")) return "repo-pds";
    if (repo.includes("Cell")) return "repo-cell";
    return "repo-github";
  }

  function showToast(message) {
    let toast = document.getElementById("supp-toast");
    if (!toast) {{
      toast = document.createElement("div");
      toast.id = "supp-toast";
      toast.className = "supp-toast";
      document.body.appendChild(toast);
    }}
    toast.textContent = message;
    toast.classList.add("visible");
    setTimeout(() => {{
      toast.classList.remove("visible");
    }}, 2500);
  }

  function copyToClipboard(text, confirmationMsg) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(confirmationMsg || "Citation copied to clipboard!");
      }).catch(() => {
        fallbackCopy(text, confirmationMsg);
      });
    } else {
      fallbackCopy(text, confirmationMsg);
    }
  }

  function fallbackCopy(text, confirmationMsg) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
      showToast(confirmationMsg || "Citation copied to clipboard!");
    } catch (err) {
      prompt("Copy to clipboard:", text);
    }
    document.body.removeChild(ta);
  }

  function filterAndSortS1() {
    let items = TABLE_S1_DATA.slice();

    // 1. Category Filter
    if (state.categoryFilter !== "All") {
      items = items.filter(r => r.Thematic_Category === state.categoryFilter);
    }

    // 2. Search Query
    if (state.searchQuery.trim() !== "") {
      const q = state.searchQuery.toLowerCase();
      items = items.filter(r => {
        return (
          r.Reference_ID.toLowerCase().includes(q) ||
          r.Citation_Number.toString().includes(q) ||
          r.Authors.toLowerCase().includes(q) ||
          r.Title.toLowerCase().includes(q) ||
          r.Journal_Or_Source.toLowerCase().includes(q) ||
          r.Thematic_Category.toLowerCase().includes(q) ||
          (r.Year && r.Year.includes(q))
        );
      });
    }

    // 3. Sorting
    items.sort((a, b) => {
      let valA = a[state.sortColumn];
      let valB = b[state.sortColumn];

      if (state.sortColumn === "Citation_Number") {
        return state.sortAsc ? valA - valB : valB - valA;
      }

      valA = (valA || "").toString().toLowerCase();
      valB = (valB || "").toString().toLowerCase();
      if (valA < valB) return state.sortAsc ? -1 : 1;
      if (valA > valB) return state.sortAsc ? 1 : -1;
      return 0;
    });

    return items;
  }

  function renderS1Table() {
    const filtered = filterAndSortS1();
    const total = filtered.length;

    // Pagination calculations
    const pageSize = state.pageSize === "All" ? total : parseInt(state.pageSize, 10);
    const totalPages = pageSize === 0 ? 1 : Math.ceil(total / pageSize);
    if (state.currentPage > totalPages) state.currentPage = Math.max(1, totalPages);

    const startIdx = (state.currentPage - 1) * pageSize;
    const endIdx = state.pageSize === "All" ? total : Math.min(startIdx + pageSize, total);
    const pageItems = filtered.slice(startIdx, endIdx);

    // Summary Text
    const summaryEl = document.getElementById("supp-s1-summary");
    if (summaryEl) {
      if (total === 0) {
        summaryEl.textContent = "No publications matched your search criteria.";
      } else {
        const rangeText = state.pageSize === "All" ? `All ${total}` : `${startIdx + 1}–${endIdx} of ${total}`;
        summaryEl.innerHTML = `Showing <strong>${rangeText}</strong> audited publications (filtered from 80 corpus total)`;
      }
    }

    // Table Body
    const tbody = document.getElementById("supp-s1-tbody");
    if (!tbody) return;

    if (pageItems.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:30px; color:var(--muted, #64748b);">No publications found matching "<em>${escapeHtml(state.searchQuery)}</em>"</td></tr>`;
      renderPagination(totalPages, total);
      return;
    }

    let rowsHtml = "";
    for (const item of pageItems) {
      const badgeCls = getCategoryBadgeClass(item.Thematic_Category);
      const linkHtml = item.DOI_Or_URL
        ? `<a class="supp-link-btn" href="${item.DOI_Or_URL}" target="_blank" rel="noopener" title="Open source publication">
             ${item.DOI_Or_URL.includes("doi.org") ? "DOI ↗" : "URL ↗"}
           </a>`
        : `<span class="supp-no-link" title="Print / Archived Reference">—</span>`;

      rowsHtml += `
        <tr>
          <td class="col-num">
            <span class="ref-badge" title="${item.Reference_ID}">[${item.Citation_Number}]</span>
          </td>
          <td class="col-authors">
            <strong>${escapeHtml(item.Authors)}</strong>
          </td>
          <td class="col-details">
            <div class="pub-title">${escapeHtml(item.Title)}</div>
            <div class="pub-journal"><em>${escapeHtml(item.Journal_Or_Source)}</em></div>
          </td>
          <td class="col-cat">
            <span class="cat-pill ${badgeCls}">${escapeHtml(item.Thematic_Category)}</span>
          </td>
          <td class="col-actions">
            ${linkHtml}
            <button class="supp-copy-btn" data-cite="${escapeAttr(item.Full_Citation)}" title="Copy full citation to clipboard">
              📋 Cite
            </button>
          </td>
        </tr>
      `;
    }
    tbody.innerHTML = rowsHtml;

    // Attach cite click listeners
    const copyBtns = tbody.querySelectorAll(".supp-copy-btn");
    copyBtns.forEach(btn => {
      btn.addEventListener("click", function() {
        const citeText = this.getAttribute("data-cite");
        copyToClipboard(citeText, "Citation copied to clipboard!");
      });
    });

    renderPagination(totalPages, total);
  }

  function renderPagination(totalPages, totalItems) {
    const container = document.getElementById("supp-pagination");
    if (!container) return;

    if (state.pageSize === "All" || totalPages <= 1) {
      container.innerHTML = "";
      return;
    }

    let html = `<div class="pagination-wrap">`;
    html += `<button class="page-btn nav-btn" data-page="${state.currentPage - 1}" ${state.currentPage === 1 ? "disabled" : ""}>‹ Previous</button>`;

    // Windowed page numbers
    let startPage = Math.max(1, state.currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);
    if (endPage - startPage < 4) {
      startPage = Math.max(1, endPage - 4);
    }

    if (startPage > 1) {
      html += `<button class="page-btn" data-page="1">1</button>`;
      if (startPage > 2) html += `<span class="page-ellipsis">…</span>`;
    }

    for (let p = startPage; p <= endPage; p++) {
      html += `<button class="page-btn ${p === state.currentPage ? "active" : ""}" data-page="${p}">${p}</button>`;
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) html += `<span class="page-ellipsis">…</span>`;
      html += `<button class="page-btn" data-page="${totalPages}">${totalPages}</button>`;
    }

    html += `<button class="page-btn nav-btn" data-page="${state.currentPage + 1}" ${state.currentPage === totalPages ? "disabled" : ""}>Next ›</button>`;
    html += `</div>`;

    container.innerHTML = html;

    const pageButtons = container.querySelectorAll(".page-btn:not([disabled])");
    pageButtons.forEach(btn => {
      btn.addEventListener("click", function() {
        const targetPage = parseInt(this.getAttribute("data-page"), 10);
        if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages) {
          state.currentPage = targetPage;
          renderS1Table();
          // Scroll gently to top of table
          const section = document.getElementById("supplementary-tables");
          if (section) section.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }

  function renderS2Cards() {
    const container = document.getElementById("supp-s2-content");
    if (!container) return;

    let html = `
      <div class="s2-header-desc">
        <p>Six curated public spaceflight, planetary magnetometer, and computational systems biology repositories synthesizing multi-omics and vector geophysical archives across Apollo, Lunar Prospector, Kaguya, ISS, and Artemis analog missions.</p>
      </div>
      <div class="s2-cards-grid">
    `;

    for (const ds of TABLE_S2_DATA) {
      const repoCls = getRepositoryBadgeClass(ds.Repository);
      html += `
        <div class="s2-card">
          <div class="s2-card-top">
            <span class="repo-badge ${repoCls}">${escapeHtml(ds.Repository)}</span>
            <span class="accession-tag">${escapeHtml(ds.Accession)}</span>
          </div>
          <h4 class="s2-target">${escapeHtml(ds.Target_System)}</h4>
          <div class="s2-platform">
            <strong>Platform / Mission:</strong> ${escapeHtml(ds.Platform_Or_Mission)}
          </div>
          <div class="s2-assays">
            <strong>Assay Types:</strong> <span class="assay-pill">${escapeHtml(ds.Assay_Types)}</span>
          </div>
          <p class="s2-desc">${escapeHtml(ds.Description)}</p>
          <div class="s2-action">
            <a class="btn primary s2-btn" href="${ds.DOI_Or_URL}" target="_blank" rel="noopener">
              Explore Repository (${escapeHtml(ds.Dataset_ID)}) ↗
            </a>
          </div>
        </div>
      `;
    }

    html += `</div>`;
    container.innerHTML = html;
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function escapeAttr(str) {
    if (!str) return "";
    return str.replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }

  function setupEventListeners() {
    // Tab switching
    const tabS1 = document.getElementById("tab-btn-s1");
    const tabS2 = document.getElementById("tab-btn-s2");
    const s1Container = document.getElementById("supp-s1-container");
    const s2Container = document.getElementById("supp-s2-container");

    if (tabS1 && tabS2) {
      tabS1.addEventListener("click", () => {
        state.activeTab = "s1";
        tabS1.classList.add("active");
        tabS2.classList.remove("active");
        if (s1Container) s1Container.style.display = "block";
        if (s2Container) s2Container.style.display = "none";
      });

      tabS2.addEventListener("click", () => {
        state.activeTab = "s2";
        tabS2.classList.add("active");
        tabS1.classList.remove("active");
        if (s1Container) s1Container.style.display = "none";
        if (s2Container) s2Container.style.display = "block";
        renderS2Cards();
      });
    }

    // Search Input
    const searchInput = document.getElementById("supp-search-input");
    const searchClear = document.getElementById("supp-search-clear");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.searchQuery = e.target.value;
        state.currentPage = 1;
        if (searchClear) {
          searchClear.style.display = state.searchQuery ? "inline-block" : "none";
        }
        renderS1Table();
      });

      if (searchClear) {
        searchClear.addEventListener("click", () => {
          searchInput.value = "";
          state.searchQuery = "";
          searchClear.style.display = "none";
          state.currentPage = 1;
          renderS1Table();
          searchInput.focus();
        });
      }
    }

    // Category Filter Dropdown
    const catSelect = document.getElementById("supp-category-select");
    if (catSelect) {
      catSelect.addEventListener("change", (e) => {
        state.categoryFilter = e.target.value;
        state.currentPage = 1;
        renderS1Table();
      });
    }

    // Page Size Selector
    const pageSizeSelect = document.getElementById("supp-page-size");
    if (pageSizeSelect) {
      pageSizeSelect.addEventListener("change", (e) => {
        state.pageSize = e.target.value;
        state.currentPage = 1;
        renderS1Table();
      });
    }

    // Sort Headers
    const sortHeaders = document.querySelectorAll(".supp-table th.sortable");
    sortHeaders.forEach(th => {
      th.addEventListener("click", function() {
        const col = this.getAttribute("data-sort");
        if (state.sortColumn === col) {
          state.sortAsc = !state.sortAsc;
        } else {
          state.sortColumn = col;
          state.sortAsc = true;
        }

        // Update UI sort arrows
        sortHeaders.forEach(h => {
          h.classList.remove("sort-asc", "sort-desc");
        });
        this.classList.add(state.sortAsc ? "sort-asc" : "sort-desc");

        renderS1Table();
      });
    });
  }

  // Initialize on DOM ready
  document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    renderS1Table();
  });

})();
