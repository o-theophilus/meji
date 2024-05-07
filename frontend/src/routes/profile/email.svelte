<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './email_form.svelte';

	export let user = {};
	export let edit_mode = false;
</script>

<span class="bold"> Email: </span>
{user.email}
{#if edit_mode}
	<BRound
		icon="edit"
		icon_size="10"
		tooltip="Edit Email"
		on:click={() => {
			$module = {
				module: Form,
				user: user
			};
		}}
	/>
{:else}
	<div />
{/if}

<style>
	.bold {
		font-weight: 700;
	}
</style>
