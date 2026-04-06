<script>
	import { Footer, Header, Nav } from '../_layout/index.js';
	let { children } = $props();
</script>

<Header />

{@render children()}
<Footer />

<div class="nav">
	<Nav />
</div>

<style>
	.nav {
		position: sticky;
		bottom: 0;

		@media screen and (min-width: 680px) {
			/* display: none; */
		}
	}
</style>
