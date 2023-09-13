<script>
	import { page } from '$app/stores';
	import { user, module } from '$lib/store.js';

	import Login from '../auth/login.svelte';
	import Signup from '../auth/signup.svelte';
	import Button from '$lib/button.svelte';
</script>

{#if !$user?.login}
	<section>
		<div class="login">
			<Button
				class="primary small"
				on:click={() => {
					$module = {
						module: Login,
						return_url: $page.url.pathname
					};
				}}
			>
				Login
			</Button>
		</div>

		<Button
			class="small"
			on:click={() => {
				$module = {
					module: Signup,
					return_url: $page.url.pathname
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

		.login {
			display: none;
		}
	}
</style>
