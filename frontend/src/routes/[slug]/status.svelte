<script>
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';
	import Form from './status_form.svelte';

	export let item = {};
	export let edit_mode = false;
</script>

{#if edit_mode}
	<div class="row">
		<span>
			Status: <span
				class="bold"
				style:color={item.status == 'draft'
					? 'var(--cl6)'
					: item.status == 'live'
					? 'var(--cl5)'
					: 'var(--cl4)'}
			>
				{item.status}</span
			>
		</span>

		{#if $user.permissions.includes('item:edit_status')}
			<BRound
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
				tooltip="Edit Status"
			>
				<SVG type="edit" size="10" />
			</BRound>
		{/if}
	</div>
{/if}

<style>
	.row {
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
