<template>
  <div class="error-container">
    <h1 class="error-title">{{ $t('errorSomethingWentWrong') }}</h1>
    <p class="error-message-grey">
      <strong>{{ $t('errorCode') }}:</strong> {{ errorCode }} <br />
      <strong>{{ $t('errorCode') }}:</strong> {{ $t(errorMessage) }}
    </p>
    <router-link :to=RoutesEnum.LOGIN.toString() class="error-link">{{ $t('goBackHome') }}</router-link>
  </div>
</template>

<script setup lang="ts">
import { RoutesEnum } from '~/config/constants'

const error = useError()
const errorCode = error.value?.statusCode || 'unknownError'
const errorMessage = error.value?.statusMessage || 'anErrorOccurred'
</script>

<style scoped lang="scss">
@use 'assets/styles/errors' as *;
</style>
