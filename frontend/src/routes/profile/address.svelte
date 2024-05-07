<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './address_form.svelte';

	export let user = {};
	export let edit_mode = false;
</script>

<span class="bold"> Address: </span>
{#if user.line && user.local_area && user.state && user.country && user.postal_code}
	{user.line}, {user.local_area}, {user.state}, {user.country}.
{:else}
	No Address
{/if}

{#if edit_mode}
	<BRound
		icon="edit"
		icon_size="10"
		tooltip="Edit Address"
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

{#if user.line && user.local_area && user.state && user.country && user.postal_code}
	<span class="bold"> Postal Code: </span>
	{user.postal_code}
{/if}

<style>
	.bold {
		font-weight: 700;
	}
</style>
