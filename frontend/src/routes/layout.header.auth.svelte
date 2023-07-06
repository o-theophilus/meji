<script>
	import { page } from '$app/stores';
	import { user, module } from '$lib/store.js';

	import Login from './auth/login.svelte';
	import Signup from './auth/signup.svelte';
	import Button from '$lib/comp/button.svelte';
</script>

{#if !$user?.login}
	<section>
		<div class="login">
			<Button
				name="Login"
				class="primary tiny"
				on:click={() => {
					$module = {
						module: Login,
						data: {
							return_url: $page.url.pathname
						}
					};
				}}
			/>
		</div>

		<Button
			name="Signup"
			class="tiny"
			on:click={() => {
				$module = {
					module: Signup,
					data: {
						return_url: $page.url.pathname
					}
				};
			}}
		/>
	</section>
{/if}

<style>
	section {
		display: flex;
		gap: var(--gap1);
	}

	@media screen and (min-width: 800px) {
		section {
			padding-left: var(--gap1);
		}

		.login {
			display: none;
		}
	}
</style>
