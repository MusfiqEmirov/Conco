/**
* Template Name: UpConstruction - v1.3.0
* Template URL: https://bootstrapmade.com/upconstruction-bootstrap-construction-website-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Mobile nav toggle
   */

  const mobileNavShow = document.querySelector('.mobile-nav-show');
  const mobileNavHide = document.querySelector('.mobile-nav-hide');

  /**
   * Minimize spacing between language code and flag in mobile navigation
   * ONLY spacing changes, no color or other property changes
   */
  function adjustMobileLanguageSpacing() {
    try {
      const isMobile = window.innerWidth <= 1279;
      
      // Find language dropdown by checking if it contains .lang-option
      const allDropdowns = document.querySelectorAll('.navbar .dropdown');
      if (!allDropdowns || allDropdowns.length === 0) return;
      
      const langDropdowns = Array.from(allDropdowns).filter(dropdown => {
        return dropdown && dropdown.querySelector('.lang-option') !== null;
      });
      
      if (langDropdowns.length === 0) return;
      
      langDropdowns.forEach(dropdown => {
        if (!dropdown) return;
        
        // Main dropdown toggle link - first direct child <a> element
        // Use children[0] since dropdown structure is <li class="dropdown"><a>...</a>
        const dropdownLink = dropdown.children[0] && dropdown.children[0].tagName === 'A' 
          ? dropdown.children[0] 
          : null;
        if (dropdownLink) {
          if (isMobile) {
            dropdownLink.style.justifyContent = 'flex-start';
            dropdownLink.style.gap = '2px';
            const span = dropdownLink.querySelector('span');
            if (span) span.style.marginRight = '0';
            const img = dropdownLink.querySelector('img');
            if (img) {
              img.style.marginLeft = '2px';
              img.style.flexShrink = '0';
            }
          } else {
            dropdownLink.style.justifyContent = '';
            dropdownLink.style.gap = '';
            const span = dropdownLink.querySelector('span');
            if (span) span.style.marginRight = '';
            const img = dropdownLink.querySelector('img');
            if (img) {
              img.style.marginLeft = '5px';
            }
          }
        }
        
        // Dropdown menu items
        const langOptions = dropdown.querySelectorAll('a.lang-option');
        if (langOptions) {
          langOptions.forEach(option => {
            if (!option) return;
            if (isMobile) {
              option.style.justifyContent = 'flex-start';
              option.style.gap = '2px';
              const img = option.querySelector('img');
              if (img) {
                img.style.marginLeft = '2px';
                img.style.flexShrink = '0';
              }
            } else {
              option.style.justifyContent = '';
              option.style.gap = '';
              const img = option.querySelector('img');
              if (img) {
                img.style.marginLeft = '5px';
              }
            }
          });
        }
      });
    } catch (error) {
      console.error('Error in adjustMobileLanguageSpacing:', error);
    }
  }

  document.querySelectorAll('.mobile-nav-toggle').forEach(el => {
    el.addEventListener('click', function(event) {
      event.preventDefault();
      mobileNavToogle();
    })
  });

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavShow.classList.toggle('d-none');
    mobileNavHide.classList.toggle('d-none');
    // Navbar açıldıqda/yandıqda spacing-i yenidən tətbiq et
    setTimeout(() => {
      try {
        adjustMobileLanguageSpacing();
      } catch (error) {
        console.error('Error in mobileNavToogle adjustMobileLanguageSpacing:', error);
      }
    }, 100);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navbar a').forEach(navbarlink => {

    if (!navbarlink.hash) return;

    let section = document.querySelector(navbarlink.hash);
    if (!section) return;

    navbarlink.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  const navDropdowns = document.querySelectorAll('.navbar .dropdown > a');

  navDropdowns.forEach(el => {
    el.addEventListener('click', function(event) {
      if (this.getAttribute('href') === '#') {
        if (window.innerWidth <= 1279) {
          event.preventDefault();
          this.classList.toggle('active');
          this.nextElementSibling.classList.toggle('dropdown-active');

          let dropDownIndicator = this.querySelector('.dropdown-indicator');
          if (dropDownIndicator) {
            dropDownIndicator.classList.toggle('bi-chevron-up');
            dropDownIndicator.classList.toggle('bi-chevron-down');
          }
        }
      }
      // Navbar dropdown açıldıqda da spacing-i tətbiq et
      setTimeout(() => {
        try {
          adjustMobileLanguageSpacing();
        } catch (error) {
          console.error('Error in dropdown click adjustMobileLanguageSpacing:', error);
        }
      }, 100);
    });
  });

  // Apply on load, resize, and when navbar opens
  // Delay initial call to ensure DOM is ready
  setTimeout(() => {
    try {
      adjustMobileLanguageSpacing();
    } catch (error) {
      console.error('Error in initial adjustMobileLanguageSpacing:', error);
    }
  }, 100);
  
  window.addEventListener('load', () => {
    setTimeout(() => {
      try {
        adjustMobileLanguageSpacing();
      } catch (error) {
        console.error('Error in load adjustMobileLanguageSpacing:', error);
      }
    }, 100);
  });
  
  window.addEventListener('resize', () => {
    try {
      adjustMobileLanguageSpacing();
    } catch (error) {
      console.error('Error in resize adjustMobileLanguageSpacing:', error);
    }
  });
  
  // MutationObserver ilə navbar açıldıqda izlə
  try {
    const bodyObserver = new MutationObserver(() => {
      if (document.body && document.body.classList.contains('mobile-nav-active')) {
        setTimeout(() => {
          try {
            adjustMobileLanguageSpacing();
          } catch (error) {
            console.error('Error in MutationObserver adjustMobileLanguageSpacing:', error);
          }
        }, 50);
      }
    });
    
    if (document.body) {
      bodyObserver.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
      });
    }
  } catch (error) {
    console.error('Error setting up MutationObserver:', error);
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('.scroll-top');
  if (scrollTop) {
    const togglescrollTop = function() {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
    window.addEventListener('load', togglescrollTop);
    document.addEventListener('scroll', togglescrollTop);
    scrollTop.addEventListener('click', window.scrollTo({
      top: 0,
      behavior: 'smooth'
    }));
  }

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox',
    touchNavigation: true,
    loop: false,
    autoplayVideos: false,
    videoAutoplay: false,
    videoMaxWidth: '1280px',
    videoMaxHeight: '720px'
  });

  /**
   * Porfolio isotope and filter
   */
  let portfolionIsotope = document.querySelector('.portfolio-isotope');

  if (portfolionIsotope) {

    let portfolioFilter = portfolionIsotope.getAttribute('data-portfolio-filter') ? portfolionIsotope.getAttribute('data-portfolio-filter') : '*';
    let portfolioLayout = portfolionIsotope.getAttribute('data-portfolio-layout') ? portfolionIsotope.getAttribute('data-portfolio-layout') : 'masonry';
    let portfolioSort = portfolionIsotope.getAttribute('data-portfolio-sort') ? portfolionIsotope.getAttribute('data-portfolio-sort') : 'original-order';

    window.addEventListener('load', () => {
      const container = document.querySelector('.portfolio-container');
      if (container) {
        let portfolioIsotope = new Isotope(container, {
          itemSelector: '.portfolio-item',
          layoutMode: portfolioLayout,
          filter: portfolioFilter,
          sortBy: portfolioSort
        });

        // Isotope instance-ini global saxla
        window.portfolioIsotopeInstance = portfolioIsotope;

        let menuFilters = document.querySelectorAll('.portfolio-isotope .portfolio-flters li');
        menuFilters.forEach(function(el) {
          el.addEventListener('click', function(e) {
            e.preventDefault();
            const activeFilter = document.querySelector('.portfolio-isotope .portfolio-flters .filter-active');
            if (activeFilter) {
              activeFilter.classList.remove('filter-active');
            }
            this.classList.add('filter-active');
            const filterValue = this.getAttribute('data-filter');
            if (portfolioIsotope && filterValue) {
              portfolioIsotope.arrange({
                filter: filterValue
              });
            }
            if (typeof aos_init === 'function') {
              aos_init();
            }
          }, false);
        });
      }

    });

  }

  /**
   * Init swiper slider with 1 slide at once in desktop view
   */
  new Swiper('.slides-1', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    }
  });

  /**
   * Init swiper slider with 2 slides at once in desktop view
   */
  new Swiper('.slides-2', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 2,
        spaceBetween: 20
      }
    }
  });

  /* Team section uses CSS ticker (no Swiper) – dayanmadan sola axır */

  /**
   * Initiate pURE cOUNTER
   */
  new PureCounter();

  /**
   * Animation on scroll function and init
   */
  function aos_init() {
    AOS.init({
      duration: 800,
      easing: 'slide',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', () => {
    aos_init();
  });

});



  document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop() || "index.html";

    document.querySelectorAll("#navbar a").forEach(link => {
      const linkPage = link.getAttribute("href");

      if (linkPage === currentPage) {
        link.classList.add("active");
      }
    });
  });

document.querySelectorAll('a[href^="mailto:"], a[href^="tel:"]').forEach(link => {
  link.addEventListener('click', function(e) {
    if (document.body.classList.contains('mobile-nav-active')) {
      mobileNavToogle();
    }
  });
});

document.querySelectorAll('.lang-option').forEach(langOption => {
  langOption.addEventListener('click', function(e) {
    e.preventDefault();
    
    const selectedLang = this.getAttribute('data-lang');
    const dropdown = this.closest('.dropdown');
    const dropdownToggle = dropdown.querySelector('a');
    const dropdownMenu = dropdown.querySelector('ul');
    const dropdownIndicator = dropdownToggle.querySelector('.dropdown-indicator');
    
    // Bayrağı ƏVVƏLCƏ dəyiş - seçilmiş dilin bayrağını dropdown menu-dən götür
    const flagImg = dropdownToggle.querySelector('img');
    const selectedFlagImg = this.querySelector('img');
    if (flagImg && selectedFlagImg) {
      flagImg.src = selectedFlagImg.src;
      flagImg.alt = selectedLang.toUpperCase();
    }
    
    // UI-ni dəyiş
    dropdownToggle.querySelector('span').textContent = selectedLang.toUpperCase();
    
    dropdownMenu.style.opacity = '0';
    dropdownMenu.style.visibility = 'hidden';
    dropdownMenu.style.pointerEvents = 'none';
    dropdownMenu.style.top = 'calc(100% + 30px)';
    
    dropdown.classList.add('dropdown-closed');
    dropdownToggle.classList.remove('active');
    
    if (dropdownIndicator) {
      dropdownIndicator.classList.remove('bi-chevron-up');
      dropdownIndicator.classList.add('bi-chevron-down');
    }
    
    // Kiçik gecikmə ver ki, bayraq dəyişikliyi görünsün
    setTimeout(() => {
      // Django-ya dil dəyişmə sorğusu göndər (GET metodu ilə)
      const currentUrl = window.location.pathname + window.location.search;
      const setLangUrl = `/i18n/setlang/?language=${selectedLang}&next=${encodeURIComponent(currentUrl)}`;
      window.location.href = setLangUrl;
    }, 50);
  });
});

document.querySelectorAll('.navbar .dropdown > a').forEach(dropdownToggle => {
  const dropdown = dropdownToggle.closest('.dropdown');
  if (dropdown && dropdown.querySelector('.lang-option')) {
    
    const dropdownState = { isOpen: false };
    
    dropdownToggle.addEventListener('click', function(e) {
      if (this.getAttribute('href') === '#') {
        if (window.innerWidth > 1279) {
          e.preventDefault();
          e.stopPropagation();
          
          const dropdownMenu = this.nextElementSibling;
          const dropdownIndicator = this.querySelector('.dropdown-indicator');
          
          if (dropdownState.isOpen) {
            dropdownMenu.style.opacity = '0';
            dropdownMenu.style.visibility = 'hidden';
            dropdownMenu.style.pointerEvents = 'none';
            dropdownMenu.style.top = 'calc(100% + 30px)';
            this.classList.remove('active');
            dropdown.classList.add('dropdown-closed');
            dropdownState.isOpen = false;
            
            if (dropdownIndicator) {
              dropdownIndicator.classList.remove('bi-chevron-up');
              dropdownIndicator.classList.add('bi-chevron-down');
            }
          } else {
            dropdownMenu.style.opacity = '1';
            dropdownMenu.style.visibility = 'visible';
            dropdownMenu.style.pointerEvents = 'auto';
            dropdownMenu.style.top = '100%';
            this.classList.add('active');
            dropdown.classList.remove('dropdown-closed');
            dropdownState.isOpen = true;
            
            if (dropdownIndicator) {
              dropdownIndicator.classList.remove('bi-chevron-down');
              dropdownIndicator.classList.add('bi-chevron-up');
            }
          }
        }
      }
    });
    
    dropdown.addEventListener('mouseleave', function() {
      if (window.innerWidth > 1279 && !dropdownState.isOpen) {
        const dropdownToggle = this.querySelector('a');
        const dropdownMenu = this.querySelector('ul');
        const dropdownIndicator = dropdownToggle.querySelector('.dropdown-indicator');
        
        dropdownMenu.style.opacity = '0';
        dropdownMenu.style.visibility = 'hidden';
        dropdownMenu.style.pointerEvents = 'none';
        dropdownMenu.style.top = 'calc(100% + 30px)';
        
        this.classList.add('dropdown-closed');
        dropdownToggle.classList.remove('active');
        
        if (dropdownIndicator) {
          dropdownIndicator.classList.remove('bi-chevron-up');
          dropdownIndicator.classList.add('bi-chevron-down');
        }
        
        setTimeout(() => {
          this.classList.remove('dropdown-closed');
          dropdownMenu.style.opacity = '';
          dropdownMenu.style.visibility = '';
          dropdownMenu.style.pointerEvents = '';
          dropdownMenu.style.top = '';
        }, 300);
      }
    });
  }
});