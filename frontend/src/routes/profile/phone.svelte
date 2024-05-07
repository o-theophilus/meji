<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './phone_form.svelte';

	export let user = {};
	export let edit_mode = false;
</script>

<span class="bold"> Phone: </span>
{#if user.phone}
	{user.phone}
{:else}
	No Phone
{/if}
{#if edit_mode}
	<BRound
		icon="edit"
		icon_size="10"
		tooltip="Edit Phone Number"
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
