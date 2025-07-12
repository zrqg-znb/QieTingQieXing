<template>
  <div class="main-layout">
    <Navbar />
    
    <main class="main-content">
      <slot></slot>
    </main>
    
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}

@media (max-width: 768px) {
  .main-content {
    padding: 10px;
  }
}
</style>