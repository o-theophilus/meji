<script>
	import { user, set_state } from '$lib/store.js';
	import { page } from '$app/stores';

	import Button from '$lib/button.svelte';

	export let page_name;
	export let actions;
	export let type;
	export let status;
</script>

<div class="status">
	<div class="buttons">
		<Button
			class="small {type == '' ? 'primary' : ''}"
			on:click={() => {
				type = '';
				status = '';
				set_state(page_name, 'status', '');
			}}
		>
			all
		</Button>

		{#each Object.keys(actions) as x}
			<Button
				class="small {x == type ? 'primary' : ''}"
				on:click={() => {
					type = x;
				}}
			>
				{x}
			</Button>
		{/each}
	</div>

	{#if $user.roles.includes('admin')}
		<div class="special">
			<Button
				class="small {$page.url.searchParams.has('admin') ? 'primary' : ''}"
				on:click={() => {
					if ($page.url.searchParams.has('admin')) {
						set_state(page_name, 'admin', '');
					} else {
						set_state(page_name, 'admin', 'true');
					}
				}}
			>
				{$page.url.searchParams.has('admin') ? 'All' : 'My'} Logs
			</Button>
		</div>
	{/if}
</div>

<style>
	.status {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		justify-content: space-between;

		margin-top: var(--sp2);
	}

	.buttons {
		display: flex;
		gap: var(--sp1);
		flex-wrap: wrap;
	}

	.special {
		padding-left: var(--sp1);
		border-left: 2px solid var(--ac3);
		flex-shrink: 0;
	}
</style>
