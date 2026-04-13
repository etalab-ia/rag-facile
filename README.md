# Rag Facile

[![Release](https://img.shields.io/github/v/release/etalab-ia/rag-facile?sort=date&style=flat-square)](https://github.com/etalab-ia/rag-facile/releases)
[![License](https://img.shields.io/github/license/etalab-ia/rag-facile?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange?style=flat-square)](https://github.com/etalab-ia/rag-facile)

```
######     #     #####     #######    #     #####  ### #       #######
#     #   # #   #     #    #         # #   #     #  #  #       #
#     #  #   #  #          #        #   #  #        #  #       #
######  #     # #  ####    #####   #     # #        #  #       #####
#   #   ####### #     #    #       ####### #        #  #       #
#    #  #     # #     #    #       #     # #     #  #  #       #
#     # #     #  #####     #       #     #  #####  ### ####### #######
```

Discutez avec vos documents PDF en utilisant le RAG (Retrieval-Augmented Generation).

## Pourquoi RAG ?

Vous avez peut-être tenté de copier-coller un long document dans un chat avec une IA. Résultat : l'IA "oublie" des parties du texte, donne des réponses vagues, ou pire — invente des informations.

**Le problème** : Les modèles de langage ont une limite de contexte. Au-delà de quelques milliers de mots, ils perdent le fil. Et pour les documents de 100+ pages, c'est impossible.

**La solution RAG** (Retrieval-Augmented Generation) fonctionne différemment :
1. Le document est découpé en petits morceaux
2. Chaque morceau est transformé en embedding (une représentation numérique)
3. Quand vous posez une question, seuls les morceaux pertinents sont récupérés
4. L'IA génère sa réponse à partir de ces extraits uniquement

**Les bénéfices** :
- 🎯 Réponses précises basées sur le contenu réel
- 📄 Citations des pages sources pour vérification
- 💰 Coût réduit (moins de tokens consommés)
- 📚 Documents de n'importe quelle taille

## Fonctionnalités

- ✅ **Conversation avec vos PDF** — Posez vos questions, obtenez des réponses avec citations de pages
- ✅ **Indexation automatique** — Fournissez une URL, le document est indexé et prêt à l'emploi
- ✅ **Génération de quiz** — Testez votre compréhension du document
- ✅ **Pas de limite de taille** — Documents de 500 pages aussi fluides que 5 pages

## Démarrage rapide

Objectif : être opérationnel en moins d'une heure.

### Prérequis

- **Node.js** >= 22.0.0
- **pnpm** — [Installation](https://pnpm.io/installation)
- **Clé API Albert** — Demandez l'accès ici : https://albert.sites.beta.gouv.fr/access/

### Installation

```bash
# Cloner le repository
git clone https://github.com/etalab-ia/rag-facile.git
cd rag-facile

# Installer les dépendances
pnpm install

# Configurer l'environnement
cp .env.example .env
```

Éditez le fichier `.env` avec vos identifiants Albert :

```env
OPENAI_API_KEY=votre-cle-albert-api
OPENAI_BASE_URL=https://albert.api.etalab.gouv.fr/v1
```

### Lancer le serveur

```bash
pnpm dev
```

Ouvrez [localhost:4111](http://localhost:4111) pour accéder à l'interface Mastra Studio.

### Premier test

1. Dans l'interface, ouvrez l'agent **"Chat with PDF"**
2. Collez l'URL d'un PDF public
3. Attendez l'indexation (quelques secondes)
4. Posez une question sur le contenu

## Architecture

```
┌─────────┐     ┌────────────┐     ┌──────────────┐
│ PDF URL │────▶│ Indexation │────▶│ Vector Store │
└─────────┘     └────────────┘     └──────────────┘
                                            │
┌──────────┐     ┌────────────┐             │
│ Question │────▶│ Recherche  │◀────────────┘
└──────────┘     └────────────┘
                       │
                       ▼
               ┌──────────────┐
               │  Albert API  │
               └──────────────┘
                       │
                       ▼
               ┌──────────────┐
               │ Réponse +    │
               │ Citations    │
               └──────────────┘
```

### Structure du projet

```
src/mastra/
├── agents/          # Agent conversationnel
├── tools/           # Outils (recherche, listage documents)
├── workflows/       # Workflow d'indexation PDF
├── lib/             # Configuration vector store
└── index.ts         # Point d'entrée Mastra
```

## Personnalisation

### Changer le modèle

La configuration se trouve dans `src/mastra/agents/pdf-chat-agent.ts` :

```typescript
model: {
  id: "albert-api/openai/gpt-oss-120b",  // Format Albert API OpenAI-compatible
  url: process.env.OPENAI_BASE_URL,
  apiKey: process.env.OPENAI_API_KEY,
}
```

Consultez la [documentation Albert](https://albert.sites.beta.gouv.fr/docs) pour les modèles disponibles.

### Changer la base vectorielle

Par défaut, Rag Facile utilise LibSQL (stockage fichier local). Mastra supporte d'autres options :

- Pinecone
- Qdrant
- Chroma
- pgvector
- Cloudflare D1

Voir la [documentation Mastra](https://mastra.ai/docs/storage/vector-databases) pour la configuration.

### Intégrer dans votre application

Rag Facile expose une API via Mastra. Utilisez le [Mastra Client SDK](https://mastra.ai/docs/server/mastra-client) pour connecter votre frontend (React, Next.js, Vue).

## Contribution

Les contributions sont bienvenues ! Ouvrez une issue ou soumettez une pull request.

## Licence

Apache-2.0 — © 2025 Etalab
