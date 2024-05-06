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

<div class="row space v_margin">
	<span class="bold"> Details </span>

	<div class="row">
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
	<div class="v_margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if item.information}
			<Marked md={item.information} />
		{:else}
			No information
		{/if}
	</div>
{/if}

<style>
	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.space {
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 700;
	}
</style>
