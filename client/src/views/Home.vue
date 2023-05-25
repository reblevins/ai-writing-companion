<template>
  <v-card>
    <v-layout>
      <v-app-bar-nav-icon icon="mdi-bookshelf" size="x-large" variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-navigation-drawer
        v-model="drawer"
        temporary
      >
        <v-app-bar title="Stories">
          <v-app-bar-nav-icon icon="mdi-bookshelf" size="x-large" variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </v-app-bar>
        <v-list class="d-flex flex-column fill-height">
          <v-list-item title="Stories"></v-list-item>
          <v-list-item v-for="(story, index) in stories" :key="story.id" :active="index === currentStoryIndex" :title="story.title" @click="fetchStory(story, index)"></v-list-item>
          <v-list-item class="mt-auto text-center" @click="createStory">New Story <v-icon icon="mdi-plus"></v-icon></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <div ref="contentTextArea" class="d-flex flex-column h-screen flex-grow-1 pb-7">
        <v-text-field class="flex-grow-0 flex-shrink-0" bg-color="white" density="compact" variant="plain" v-model="currentStory.title"></v-text-field>
        <v-select
          v-model="currentScene"
          class="flex-grow-0 flex-shrink-0"
          label="Scene"
          :items="currentStory.scenes"
          item-text="title"
          item-value="index"
          variant="underlined"
          return-object
        >
          <template #append-item>
            <v-btn @click="createScene">New Scene <v-icon icon="mdi-plus"></v-icon></v-btn>
          </template>
        </v-select>
        <!-- <v-card ref="contentTextArea" class="flex-grow-1 flex-shrink-0 mb-3" variant="outlined">
          <v-card-text> -->
            <v-textarea
              class="flex-grow-1 flex-shrink-0 mb-3"
              v-model="currentScene.content"
              :rows="contentTextAreaRows"
              variant="outlined"
            ></v-textarea>
          <!-- </v-card-text>
        </v-card> -->
        <v-card class="suggestion flex-grow-0 flex-shrink-0" variant="outlined" :loading="loading">
          <v-card-title>Suggestion</v-card-title>
          <v-card-text v-if="suggestion != ''">{{ suggestion }}</v-card-text>
          <v-card-text v-else class="font-italic text-caption">Click "Generate" to generate a new suggestion.</v-card-text>
          <v-card-actions v-if="suggestion != ''">
            <v-btn @click="insertSuggestion">Insert</v-btn>
            <v-btn @click="generate">Try Again</v-btn>
            <v-btn @click="suggestion = ''">Cancel</v-btn>
          </v-card-actions>
          <v-card-actions v-else>
            <v-btn @click="generate">Generate</v-btn>
            <v-btn @click="updateStory">Save</v-btn>
          </v-card-actions>
        </v-card>
      </div>
      <v-app-bar-nav-icon variant="text" icon="mdi-cog" @click.stop="settings = !settings"></v-app-bar-nav-icon>
      <v-navigation-drawer
        class="pa-3"
        v-model="settings"
        permanent
        location="right"
        width="512"
      >
        <v-app-bar-nav-icon variant="text" @click.stop="settings = !settings">
          <v-icon icon="mdi-cog" size="large"></v-icon>
        </v-app-bar-nav-icon>
        <v-tabs
          v-model="settingsTab"
          align-tabs="left"
        >
          <v-tab value="summary_settings">Summary</v-tab>
          <v-tab value="story_settings">Story</v-tab>
        </v-tabs>
        <v-window v-model="settingsTab">
          <v-window-item value="summary_settings">
            <v-text-field label="Title" v-model="currentScene.title"></v-text-field>
            <v-textarea label="Summary" v-model="currentScene.summary" rows="10" auto-grow></v-textarea>
          </v-window-item>
          <v-window-item value="story_settings">
            <v-text-field label="Title" v-model="currentStory.title"></v-text-field>
            <v-textarea label="Summary" v-model="currentStory.summary" rows="10"></v-textarea>

            <v-btn color="red" @click="deleteStory">Delete Story</v-btn>
          </v-window-item>
        </v-window>
      </v-navigation-drawer>
    </v-layout>
  </v-card>
  <v-snackbar
    v-model="statusDialogOpen"
    multi-line
  >
    {{ statusText }}

    <template v-slot:actions>
      <v-btn
        color="red"
        variant="text"
        @click="statusDialogOpen = false"
      >
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import axios from 'axios'

const drawer = ref(false)
const settings = ref(false)
const loading = ref(false)
const stories = ref([])
const currentStory = ref({
  id: null,
  title: '',
  genre: '',
  summary: '',
  content: '',
  characters: '',
  setting: '',
  scenes: []
})
const currentStoryIndex = ref(0)
const currentSceneIndex = ref(0)
const prompts = ref([])
const suggestion = ref('')
const content = ref('')
const contentTextArea = ref(null)
const contentTextAreaRows = ref(1)
const statusDialogOpen = ref(false)
const statusText = ref('')
const settingsTab = ref('summary_settings')
const apiUrl = 'http://127.0.0.1'
const apiPort = 5001

onMounted(async () => {
  fetchStories()

  setTimeout(() => {
    console.log(contentTextArea.value.clientHeight)
    contentTextAreaRows.value = Math.floor((contentTextArea.value.clientHeight - 183) / 31)
  }, 500)
})

const updateContent = (event) => {
  currentScene.value.content = event.target.textContent;
}

const currentScene = ref({
  title: '',
  summary: '',
  content: ''
})

const generate = async () => {
  loading.value = true
  const body = {
    prompts: currentStory.value.content?.trim() || '',
    title: currentStory.value.title,
    genre: currentStory.value.genre,
    summary: currentStory.value.summary,
    scene: currentScene.value.summary + '\n\n' + currentScene.value.content,
    // characters: characters.value,
    // setting: setting.value,
  }
  console.log(body)
  const response = await axios.post(`${apiUrl}:${apiPort}/generate`, body)
  prompts.value = response.data.prompts
  suggestion.value = response.data.suggestion

  if (response.data.error) {
    loading.value = false
    statusText.value = response.data.error
    statusDialogOpen.value = true
    console.log(response.data.error)
    return
  }

  content.value = prompts.value[prompts.value.length - 1].content
  
  // if the last character is a period with no space, add a space
  // if (content.value.slice(-1) === '.') {
  //   content.value += ' '
  // }
  loading.value = false
}

// Retrieve a list of stories from the api
const fetchStories = async () => {
  const response = await axios.get(`${apiUrl}:${apiPort}/stories`)
  stories.value = response.data
  console.log(stories.value)
  if (stories.value.length > 0) {
    fetchStory(stories.value[0])
  }
}

// Fetch a story
const fetchStory = async (story, index) => {
  const response = await axios.get(`${apiUrl}:${apiPort}/stories/${story.id}`)
  currentStory.value = response.data
  currentStoryIndex.value = index
  if (currentStory.value.content === null) {
    currentStory.value.content = ''
  }
  if (currentScene.value.id === undefined) {
    currentSceneIndex.value = currentStory.value.scenes.length - 1
    currentScene.value = currentStory.value.scenes[currentSceneIndex.value]
  }
  if (currentScene.value.content === null) {
    currentScene.value.content = ''
  }
  drawer.value = false
}

// Create a new story
const createStory = async () => {
  const response = await axios.post(`${apiUrl}:${apiPort}/stories`, { title: 'Untitled' })
  stories.value.push(response.data)
}

// Update a story
const updateStory = async () => {
  console.log(currentStory.value.id)
  const response = await axios.put(`${apiUrl}:${apiPort}/stories/${currentStory.value.id}`, currentStory.value)
  fetchStories()
}

// Delete a story
const deleteStory = async () => {
  const response = await axios.delete(`${apiUrl}:${apiPort}/stories/${currentStory.value.id}`)
  fetchStories()
}

const insertSuggestion = (index) => {
  // If the last character isn't a space, add one
  if (currentScene.value.content.slice(-1) !== ' ') {
    console.log('inserting suggestion', content.value.slice(-1))
    currentScene.value.content += ' '
  }
  currentScene.value.content += suggestion.value
  suggestion.value = ''
}

const showErrorAlert = (message) => {
  
}

const createScene = () => {
  currentStory.value.scenes.push({
    title: '',
    summary: '',
    content: ''
  })
  currentSceneIndex.value = currentStory.value.scenes.length - 1
}
</script>

<style lang="scss" scoped>
#editor, .suggestion {
  border: 1px solid #ccc;
  outline: none;
}
#editor div {
  margin-bottom: 12px;
}
</style>