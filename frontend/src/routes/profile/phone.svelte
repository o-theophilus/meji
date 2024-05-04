<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './phone_form.svelte';
	import SVG from '$lib/svg.svelte';

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
		tooltip="Edit Phone Number"
		on:click={() => {
			$module = {
				module: Form,
				user: user
			};
		}}
	>
		<SVG type="edit" size="10" />
	</BRound>
{:else}
	<div />
{/if}

<style>
	.bold {
		font-weight: 700;
	}
</style>
