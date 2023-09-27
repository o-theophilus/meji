<script>
	import { user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	import Add from './_add.svelte';
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<Button
			class="small"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		>
			Add
		</Button>
	</div>
{/if}

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
