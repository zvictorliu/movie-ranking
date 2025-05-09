import { defineStore } from 'pinia';

export const useViewStore = defineStore('view', {
  state: () => ({
    isMovieView: true, // 当前是否显示影片视图
  }),
  actions: {
    toggleView() {
        console.log('toggleView in view.js');
      this.isMovieView = !this.isMovieView;
    },
  },
});