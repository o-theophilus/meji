<script>
	import { user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Add from './_add.svelte';
</script>

{#if $user && $user.roles.includes('admin')}
	<div class="block">
		<Button
			name="Add"
			class="tiny"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		/>
	</div>
{/if}

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
