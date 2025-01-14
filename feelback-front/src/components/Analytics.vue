<template>
  <v-container>
    <!-- Videos Section -->
    <v-row dense class="video-container">
      <v-col cols="8" style="height: 100%">
        <video muted v-show="showVideoLabels" id="video1">
          <source :src="getVideoSource(reactionVideoID, true)" type="video/webm" />
          Sorry, your browser doesn't support embedded videos.
        </video>
        <video muted v-show="!showVideoLabels" id="video3">
          <source :src="getVideoSource(reactionVideoID, false)" type="video/webm" />
          Sorry, your browser doesn't support embedded videos.
        </video>
      </v-col>
      <v-col cols="4" style="height: 100%">
        <video muted id="video2">
          <source :src="getTrailerVideoSource(reactionVideoID)" type="video/webm" />
          Sorry, your browser doesn't support embedded videos.
        </video>
      </v-col>
    </v-row>

    <!-- Video Controls section -->
    <v-row dense>
      <v-col cols="12">
        <v-slider
          @change="seekbarChanged"
          min="0"
          max="100"
          v-model="seekedValue"
          dense
          hide-details
        ></v-slider>
      </v-col>
      <v-col cols="12">
        <v-row dense justify="space-between" style="padding: 0px 10px 20px">
          <!-- Current time of the video :- Calculated from video 1 only -->
          <v-col cols="2">
            {{ Math.floor(this.currentPlaybackTime / 60) }}:{{
              Math.floor((this.currentPlaybackTime % 60) / 10)
            }}{{ Math.floor((this.currentPlaybackTime % 60) % 10) }}
          </v-col>
          <v-col cols="8">
            <v-row dense justify="center" align="center">
              <v-col cols="auto" class="centralize">
                <v-btn icon @click="playPauseVideo" class="mr-3">
                  <v-icon v-if="!playVideo" large color="blue"> mdi-play </v-icon>
                  <v-icon v-else large color="blue"> mdi-pause </v-icon>
                </v-btn>
                <span>
                  <v-switch @change="showAnnotation" inset label="Annotated"></v-switch>
                </span>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="2" style="text-align: end"
            >{{ Math.floor(this.fullPlaybackTime / 60) }}:{{
              Math.floor((this.fullPlaybackTime % 60) / 10)
            }}{{ Math.floor((this.fullPlaybackTime % 60) % 10) }}</v-col
          >
        </v-row>
      </v-col>
    </v-row>

    <!-- Tabs section -->
    <v-tabs grow dark class="tabs" v-model="tab">
      <v-tab> Overall </v-tab>
      <v-tab> In-Depth </v-tab>
      <v-tab> Key Moments </v-tab>
    </v-tabs>

    <!-- Tab items Section -->
    <v-tabs-items v-model="tab" class="pt-5">
      <v-tab-item key="1">
        <OverallStats :stats="OverallStats" />
      </v-tab-item>
      <v-tab-item key="2">
        <InDepthAnalytics
          :InDepthStats="InDepthStats ? InDepthStats.persons : []"
          :moodData="InDepthStats ? InDepthStats.mood : []"
        />
      </v-tab-item>
      <v-tab-item key="3">
        <KeyMoments :KeyMoments="KeyMoments" :seekToCertainSecond="seekToCertainSecond" />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import InDepthAnalytics from './InDepthAnalytics.vue';
import OverallStats from './OverallStats.vue';
import KeyMoments from './KeyMoments.vue';
import api from '../api/index';

export default {
  components: {
    InDepthAnalytics,
    OverallStats,
    KeyMoments,
  },

  props: {
    reactionVideoID: String,
    trailerVideoID: String,
  },

  data: () => ({
    // Page variables
    tab: null,
    // Videos
    mediaOne: null,
    mediaTwo: null,
    mediaThree: null,
    // Video Controls
    playVideo: false,
    seekedValue: 0,
    currentPlaybackTime: 0,
    fullPlaybackTime: 0,
    showVideoLabels: false,
    // Analytics Data
    OverallStats: null,
    KeyMoments: null,
    InDepthStats: null,
  }),

  methods: {
    playPauseVideo() {
      // Set play to pause and vice versa
      this.playVideo = !this.playVideo;

      // Play and pause videos
      if (this.playVideo) {
        this.mediaOne.play();
        this.mediaTwo.play();
        this.mediaThree.play();
      } else {
        this.mediaOne.pause();
        this.mediaTwo.pause();
        this.mediaThree.pause();
      }
    },

    stopVideo() {
      // Pause both videos
      this.mediaOne.pause();
      this.mediaTwo.pause();
      this.mediaThree.pause();

      // Set the time in both videos to zero
      this.mediaOne.currentTime = 0;
      this.mediaTwo.currentTime = 0;
      this.mediaThree.currentTime = 0;

      // Set play video to false
      this.playVideo = false;
    },

    seekbarChanged() {
      this.mediaOne.currentTime = (this.seekedValue / 100) * this.mediaOne.duration;
      this.mediaTwo.currentTime = (this.seekedValue / 100) * this.mediaTwo.duration;
      this.mediaThree.currentTime = (this.seekedValue / 100) * this.mediaThree.duration;
    },

    seekToCertainSecond(seekSecond) {
      this.mediaOne.currentTime = seekSecond;
      this.mediaTwo.currentTime = seekSecond;
      this.mediaThree.currentTime = seekSecond;
    },

    setVideoFullPlaybackTime() {
      const timer = setInterval(() => {
        if (this.mediaOne.readyState > 0) {
          this.fullPlaybackTime = this.mediaOne.duration;
          clearInterval(timer);
        }
      }, 200);
    },

    getInsights() {
      // Get video ID from the url
      const videoID = this.$route.params.id;

      // Get OverAll Stats
      api.getVideoInsights(videoID).then((response) => {
        this.OverallStats = response.data;
      });
    },

    getKeymoments() {
      // Get video ID from the url
      const videoID = this.$route.params.id;

      // Get OverAll Stats
      api.getVideoKeymoments(videoID).then((response) => {
        this.KeyMoments = response.data;
      });
    },

    getAnalytics() {
      // Get video ID from the url
      const videoID = this.$route.params.id;

      // Get OverAll Stats
      api.getVideoAnalytics(videoID).then((response) => {
        this.InDepthStats = response.data;
      });
    },

    getVideoSource(videoID, annotated) {
      return api.getVideoURL(videoID, annotated);
    },

    getTrailerVideoSource(videoID) {
      return api.getTrailerVideoURL(videoID);
    },

    showAnnotation(value) {
      // Sync all videos
      const seekSecond = value ? this.mediaThree.currentTime : this.mediaOne.currentTime;
      this.seekToCertainSecond(seekSecond);

      // Change value
      this.showVideoLabels = value;
    },
  },

  async mounted() {
    // Select the two videos and save them to data
    this.mediaOne = document.querySelector('#video1');
    this.mediaTwo = document.querySelector('#video2');
    this.mediaThree = document.querySelector('#video3');

    // Set the full video playback time
    this.setVideoFullPlaybackTime();

    // Add event listeners to set current time and current seek time
    this.mediaOne.addEventListener('timeupdate', () => {
      this.currentPlaybackTime = this.mediaOne.currentTime;
      this.seekedValue = (this.currentPlaybackTime / this.fullPlaybackTime) * 100;
    });

    // Ended event to stop the videos
    this.mediaOne.addEventListener('ended', this.stopVideo);
    this.mediaTwo.addEventListener('ended', this.stopVideo);
    this.mediaThree.addEventListener('ended', this.stopVideo);

    // Get Analytics data
    this.getInsights();
    this.getKeymoments();
    this.getAnalytics();
  },
};
</script>

<style>
.center-text {
  justify-content: center;
  text-align: center;
}

.video-container {
  height: 400px;
}

.video-container video {
  height: 100%;
  width: 100%;
}

.centralize {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
