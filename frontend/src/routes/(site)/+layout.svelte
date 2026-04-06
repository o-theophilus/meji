<script>
	import { Footer, Header, Nav } from '../_layout/index.js';
	let { children } = $props();
</script>

<div class="header">
	<Header />
</div>

{@render children()}
<Footer />

<div class="nav">
	<Nav />
</div>

<style>
	.header {
		z-index: 1;
		@media screen and (min-width: 800px) {
			position: sticky;
			top: 0;
		}
	}

	.nav {
		position: sticky;
		bottom: 0;

		@media screen and (min-width: 800px) {
			display: none;
		}
	}
</style>
