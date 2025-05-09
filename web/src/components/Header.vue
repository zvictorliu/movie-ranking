<template>
    <header class="app-header">
      <div class="logo" @click="goToHome">
        <img src="/home-button.png" alt="Logo" />
      </div>
      <h1 class="title" >影片排行榜</h1>
      
    </header>
</template>

<script>
export default {
  name: "Header",
  methods: {
    goToHome() {
      this.$router.push({ name: "HomePage" }); // 返回主页 [[6]]
    },
    
  },
};
</script>

<style scoped>
.app-header {
  background-color: #42b983;
  padding: 10px 20px;
  align-items: center;
  display: flex;
}

.logo img {
  width: 50px;
  cursor: pointer;
}

.title {
  color: white;
  font-size: 24px;
  margin: 0 10px;
}
</style>