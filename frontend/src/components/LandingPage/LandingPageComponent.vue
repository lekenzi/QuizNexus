<template>
  <div class="greeting">
    <h1>{{ displayText }}<span class="cursor" v-if="isTyping">|</span></h1>
  </div>
</template>

<script>
export default {
  name: "LandingPage",
  components: {},
  data() {
    return {
      fullText: "QuizNexus!",
      displayText: "",
      isTyping: true,
      typingSpeed: 150,
    };
  },
  mounted() {
    this.typeText();
  },
  methods: {
    typeText() {
      let currentIndex = 0;
      const typeInterval = setInterval(() => {
        if (currentIndex < this.fullText.length) {
          this.displayText += this.fullText.charAt(currentIndex);
          currentIndex++;
        } else {
          clearInterval(typeInterval);
          this.isTyping = false;

          setInterval(() => {
            this.isTyping = !this.isTyping;
          }, 500);
        }
      }, this.typingSpeed);
    },
  },
};
</script>

<style scoped>
.greeting {
  justify-content: center !important;
  height: 8vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent;
}

.greeting h1 {
  color: black;
  font-weight: bold;
}

.cursor {
  display: inline-block;
  font-weight: 100;
  font-size: xx-large;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
</style>
