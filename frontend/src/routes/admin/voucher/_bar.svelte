<script>
	import { user, module } from '$lib/store.js';

	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	import Add from './_add.svelte';
</script>

{#if $user && $user.roles.includes('admin')}
	<Body>
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
	</Body>
{/if}

<style>
	.block {
		display: flex;
		gap: var(--gap1);
	}
</style>
