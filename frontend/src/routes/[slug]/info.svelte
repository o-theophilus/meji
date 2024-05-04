<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Marked from '$lib/marked.svelte';
	import Form from './info_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open = true && item.information;
</script>

<div class="horizontal bold">
	Details
	<div class="horizontal">
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
		{#if edit_mode && $user.permissions.includes('item:edit_info')}
			<BRound
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
				tooltip="Edit Details"
			>
				<SVG type="edit" size="10" />
			</BRound>
		{/if}
	</div>
</div>
{#if open}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if item.information}
			<Marked md={item.information} />
		{:else}
			No information
		{/if}
	</div>
{/if}

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 700;
	}
</style>
