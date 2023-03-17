<template>
  <v-card>
    <v-layout>
      <v-app-bar-nav-icon icon="mdi-bookshelf" size="x-large" variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-navigation-drawer
        v-model="drawer"
        temporary
      >
        <v-app-bar title="Application bar">
          <v-app-bar-nav-icon icon="mdi-bookshelf" size="x-large" variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </v-app-bar>
        <v-list>
          <v-list-item title="Navigation drawer"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-main class="h-screen" style="padding-top: 0;">
        <v-container class="d-flex flex-column">
          <v-row>
            <v-col cols="12" style="height: 70px;">
              <v-text-field bg-color="white" density="compact" variant="plain" v-model="title"></v-text-field>
            </v-col>
            <v-col cols="12" ref="contentTextArea" style="height: calc(100vh - 140px) !important;">
              <v-textarea
                v-model="content"
                class="h-100"
                style="height: 100%;"
                bg-color="white"
                variant="plain"
                :loading="loading"
                :rows="contentTextAreaRows"
              ></v-textarea>
            </v-col>
            <v-col cols="12" style="height: 70px;">
              <v-btn @click="generate">Generate</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
      <v-app-bar-nav-icon variant="text" icon="mdi-cog" @click.stop="settings = !settings"></v-app-bar-nav-icon>
      <v-navigation-drawer
        v-model="settings"
        permanent
        location="right"
        width="512"
      >
        <v-app-bar-nav-icon variant="text" @click.stop="settings = !settings">
          <v-icon icon="mdi-cog" size="large"></v-icon>
        </v-app-bar-nav-icon>
        <v-list>
          <v-list-item title="Settings">
            <v-text-field label="Genre" v-model="genre"></v-text-field>
            <v-textarea label="Summary" v-model="summary" rows="10"></v-textarea>
            <!-- <v-text-field label="Characters" v-model="characters"></v-text-field>
          <v-text-field label="Setting" v-model="setting"></v-text-field> -->
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-layout>
  </v-card>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import axios from 'axios'

import InputBox from '@/components/InputBox.vue';

const drawer = ref(false)
const settings = ref(false)
const loading = ref(false)
const prompts = ref([])
const content = ref('SCENE: On the bridge of The Wayward Star.')
const contentTextArea = ref()
const title = ref('The Wayward Star')
const genre = ref('Science Fiction')
const summary = ref(`"The Wayward Star" is an interstellar spaceship, one of the most advanced in the galaxy, with a unique characteristic: it is sentient. It has a mind of its own and is known to be slightly eccentric. The ship is equipped with the latest technology, and it can travel faster than light.

The ship is under the command of Captain Jane, a fearless leader who is respected by the crew. The rest of the crew is made up of a rag-tag group of humans and aliens, each with their own set of skills and quirks. There's Ben, the ship's engineer, who's always tinkering with something; Sarah, the ship's medic, who's both tough and caring; and Zax, a humanoid alien with a mischievous streak.

"The Wayward Star" is on a mission to explore the galaxy and make contact with other intelligent life forms. As they journey through the stars, they encounter a variety of strange and fascinating creatures. Some are friendly, while others are hostile, but the crew always manages to find a way to navigate through the challenges.

However, as they continue their journey, the ship's eccentricity becomes more pronounced. It starts to develop its own personality and even a sense of humor. It starts to play practical jokes on the crew, and sometimes it makes decisions that are not in their best interest.

Despite this, the crew remains loyal to the ship, and they come to love it like a member of their family. They realize that "The Wayward Star" is more than just a spaceship; it's a living being, with its own hopes and fears, and they are honored to be a part of its journey.

As they continue their mission, the crew faces many challenges, both external and internal. They must battle dangerous alien creatures, navigate treacherous asteroid fields, and deal with their own personal demons. But through it all, they stick together and rely on each other, and the ship's eccentricity adds a unique flavor to their adventures.

In the end, "The Wayward Star" and its crew complete their mission, having explored more of the galaxy than anyone ever thought possible. And though they may have faced many dangers along the way, they all agree that it was worth it, for the experiences they shared and the friendships they forged will last a lifetime.`)
const characters = ref('')
const setting = ref('')

onMounted(async () => {
  setTimeout(() => {
    contentTextAreaRows.value = Math.floor(contentTextArea.value.$el.clientHeight / 26)
  }, 100)
})

const generate = async () => {
  loading.value = true
  const body = {
    prompts: content.value,
    title: title.value,
    genre: genre.value,
    summary: summary.value,
    // characters: characters.value,
    // setting: setting.value,
    // scene: scene.value
  }
  const { data } = await axios.post('http://localhost:5000', body)
  content.value = data.map((prompt) => {
    if (prompt.role !== 'system') {
      return prompt.content
    }
  }).join('')
  // if the last character is a period with no space, add a space
  if (content.value.slice(-1) === '.') {
    content.value += ' '
  }
  loading.value = false
}

const contentTextAreaRows = ref()

watch(content, (val) => {
  // Log height of contentTextArea
})
</script>
