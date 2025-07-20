<template>
  <IndexPageNav />
  <div style="">
    <router-view style="position: fixed" />
  </div>
</template>
<script>
import IndexPageNav from "./components/LandingPage/IndexPageNav.vue";

export default {
  name: "IndexPageView2",
  components: {
    IndexPageNav,
  },
  mounted() {},
};
</script>

<style>
body,
html {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  min-height: 100vh;
  background-image: url("./../public/img/landingpagebg.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.greeting {
  text-align: center;
  color: rgb(0, 0, 0);
  margin: 20vh auto 0 auto;
  border-radius: 20px;
  background-color: rgb(255, 255, 255);
  width: 800px;
  max-width: 90vw;
  padding: 2rem 1.5rem;
  box-shadow: 0 4px 16px rgba(0, 00, 0.08);
}
.greeting h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}
.greeting p {
  font-size: 1.5rem;
}
</style>
