import csv
import matplotlib.pyplot as plt

# Ouvrir le fichier "extrait.txt"
with open("DumpFile.txt", "r") as fichier:
    ipsr, ipde, longueur, flag, seq, heure = [], [], [], [], [], []
    flagcounterP, flagcounterS, flagcounter = 0, 0, 0
    framecounter, requestcounter, replycounter = 0, 0, 0
    seqcounter, ackcounter, wincounter = 0, 0, 0

    for ligne in fichier:
        split = ligne.split(" ")

        if "IP" in ligne:
            framecounter += 1

            if "[P.]" in ligne:
                flag.append("[P.]")
                flagcounterP += 1
            elif "[.]" in ligne:
                flag.append("[.]")
                flagcounter += 1
            elif "[S]" in ligne:
                flag.append("[S]")
                flagcounterS += 1

            if "seq" in ligne:
                seqcounter += 1
                seq.append(split[8])

            if "win" in ligne:
                wincounter += 1

            if "ack" in ligne:
                ackcounter += 1

            ipsr.append(split[2])
            ipde.append(split[4])
            heure.append(split[0])

            if "length" in ligne:
                split = ligne.split(" ")
                longueur.append(split[-2] if "HTTP" in ligne else split[-1])

            if "ICMP" in ligne:
                if "request" in ligne:
                    requestcounter += 1
                elif "reply" in ligne:
                    replycounter += 1

# Ajouter une vérification pour éviter la division par zéro
globalreqrepcounter = replycounter + requestcounter
if globalreqrepcounter != 0:
    req = requestcounter / globalreqrepcounter
    rep = replycounter / globalreqrepcounter
else:
    req = rep = 0

globalflagcounter = flagcounter + flagcounterP + flagcounterS
P = flagcounterP / globalflagcounter
S = flagcounterS / globalflagcounter
A = flagcounter / globalflagcounter

flagcounter = [flagcounter]
flagcounterP = [flagcounterP]
flagcounterS = [flagcounterS]
framecounter = [framecounter]
requestcounter = [requestcounter]
replycounter = [replycounter]
seqcounter = [seqcounter]
ackcounter = [ackcounter]
wincounter = [wincounter]

# Générer les diagrammes circulaires
# Diagramme des drapeaux
labels_flags = ['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)']
sizes_flags = [flagcounterP[0], flagcounterS[0], flagcounter[0]]
explode_flags = (0.1, 0, 0)  # Explosion du premier segment
fig_flags, ax_flags = plt.subplots()
ax_flags.pie(sizes_flags, explode=explode_flags, labels=labels_flags, autopct='%1.1f%%', startangle=90)
ax_flags.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.savefig('diagramme_drapeaux.png')
plt.close(fig_flags)

# Diagramme des requêtes et réponses
labels_requests_replies = ['Request', 'Reply']
sizes_requests_replies = [requestcounter[0], replycounter[0]]
explode_requests_replies = (0.1, 0)  # Explosion du premier segment
fig_requests_replies, ax_requests_replies = plt.subplots()
ax_requests_replies.pie(sizes_requests_replies, explode=explode_requests_replies, labels=labels_requests_replies, autopct='%1.1f%%', startangle=90)
ax_requests_replies.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.savefig('diagramme_requetes_reponses.png')
plt.close(fig_requests_replies)

# Contenu de la page Markdown
markdown_content = f'''
# Traitement des données

## Bineta - Projet SAE 15

Sur cette page web, nous vous présentons les informations et données pertinentes trouvées dans le fichier à traiter.

### Nombre total de trames échangées
{framecounter[0]}

### Drapeaux (Flags)
- Nombre de flags [P] (PUSH): {flagcounterP[0]}
- Nombre de flags [S] (SYN): {flagcounterS[0]}
- Nombre de flag [.] (ACK): {flagcounter[0]}

![Diagramme des drapeaux](diagramme_drapeaux.png)

### Nombre de requêtes et réponses
- Request: {requestcounter[0]}
- Reply: {replycounter[0]}

![Diagramme des requêtes et réponses](diagramme_requetes_reponses.png)

### Statistiques entre seq, win et ack
- Nombre de seq: {seqcounter[0]}
- Nombre de win: {wincounter[0]}
- Nombre de ack: {ackcounter[0]}
'''

# Ouvrir un fichier CSV pour les données extraites du fichier texte non traité
with open('donnees.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'])
    writer.writerows(zip(heure, ipsr, ipde, flag, seq, longueur))

# Ouvrir un fichier CSV pour les statistiques générales
with open('Stats.csv', 'w', newline='') as fichier2:
    writer = csv.writer(fichier2)
    writer.writerow(['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames',
                     'Nombre de request', 'Nombre de reply', 'Nombre de sequence', 'Nombre de acknowledg', 'Nombre de window'])
    writer.writerows(zip(flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter))

# Créer un fichier Markdown
with open("data.md", "w") as markdown_file:
    markdown_file.write(markdown_content)
    print("Page Markdown créée avec succès.")