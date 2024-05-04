<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './email_form.svelte';
	import SVG from '$lib/svg.svelte';

	export let user = {};
	export let edit_mode = false;
</script>

<span class="bold"> Email: </span>
{user.email}
{#if edit_mode}
	<BRound
		tooltip="Edit Email"
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
