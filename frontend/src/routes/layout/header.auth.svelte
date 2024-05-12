<script>
	import { user, module } from '$lib/store.js';

	import Login from '../auth/login.svelte';
	import Signup from '../auth/signup.svelte';
	import Button from '$lib/button/button.svelte';
</script>

{#if !$user?.login}
	<section>
		<div class="login">
			<Button
				primary
				on:click={() => {
					$module = {
						module: Login
					};
				}}
			>
				Login
			</Button>
		</div>

		<Button
			on:click={() => {
				$module = {
					module: Signup
				};
			}}
		>
			Signup
		</Button>
	</section>
{/if}

<style>
	section {
		display: flex;
		gap: var(--sp1);
	}

	@media screen and (min-width: 800px) {
		section {
			padding-left: var(--sp1);
		}
	}
</style>
